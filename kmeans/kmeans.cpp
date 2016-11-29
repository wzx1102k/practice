#include <opencv/cv.hpp>
#include <opencv/highgui.h>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

#define SRC_IMG argv[1]
#define KNUM argv[2]
#define DES_IMG argv[3]

#define KDEBUG_ENABLE 1
#if KDEBUG_ENABLE
	#define KDEBUG(x) \
	do{ \
		x; \
	} while(0);
#else
	#define KDEBUG(x)
#endif
struct GrayPoint{
	int x;
	int y;
	int v;
	int label;
};

struct SrcPoint {
	int x;
	int y;
	int rv;
	int bv;
	int gv;
	double rb;
	double rg;
	double gb;
	int label;
};

vector<GrayPoint> gray_means;
vector<SrcPoint> src_means;
vector<GrayPoint> gray_cluster;
vector<SrcPoint>  src_cluster;

static double kmeans_calDict(vector<double> dict1, vector<double> dict2);

int kmeans_src_init(vector<SrcPoint> &means, vector<SrcPoint> &cluster, int knum) {
	int cnt = 0;
	if((cluster.size() < 2) || (knum < 2)) {
		printf("Kmeans init para error!\n");
		return -1;
	}

	vector<SrcPoint> xcluster;
	cluster[0].rb = (double)cluster[0].rv/(double)cluster[0].bv;
	cluster[0].rg = (double)cluster[0].rv/(double)cluster[0].gv;
	cluster[0].gb = (double)cluster[0].gv/(double)cluster[0].bv;
	xcluster.push_back(cluster[0]);
	for(int i=0; i<cluster.size();i++) {
		cluster[i].rb = (double)cluster[i].rv/(double)cluster[i].bv;
		cluster[i].rg = (double)cluster[i].rv/(double)cluster[i].gv;
		cluster[i].gb = (double)cluster[i].gv/(double)cluster[i].bv;
		if(xcluster[cnt].x != cluster[i].x) {
			xcluster.push_back(cluster[i]);
			cnt ++; 
		} else {
			continue;
		}
		//KDEBUG(printf("%d: x = %d, y = %d, v = %d\n", cnt, xcluster[cnt].x, xcluster[cnt].y, xcluster[cnt].v));
	}

	KDEBUG(printf("xcluster size = %d\n", (int)xcluster.size()));
	for(int i=0; i<knum; i++) {
		means.push_back(xcluster[i*((cnt-1)/(knum-1))]);
		means[i].label = i;
		KDEBUG(printf("means init: x=%d, y=%d, rv=%d, gv=%d, bv=%d, rg=%f, rb=%f, gb=%f, label=%d\n", means[i].x, means[i].y, means[i].rv, means[i].gv, means[i].bv, means[i].rg, means[i].rb, means[i].gb, means[i].label));			
	}

	return 0;
}

int kmeans_src_update(vector<SrcPoint> &means, vector<SrcPoint> cluster, vector<int> &cnt) {
	SrcPoint point;
	point.x = 0;
	point.y = 0;
	point.gv = 0;
	point.bv = 0;
	point.rv = 0;
	point.rb = 0;
	point.rg = 0;
	point.gb = 0;
	point.label = 0;
	int index = 0;

	means.assign(means.size(), point);
	for(int i=0; i<cluster.size(); i++) {
		index = cluster[i].label;
		means[index].x += cluster[i].x;
		means[index].y += cluster[i].y;
		means[index].rv += cluster[i].rv;
		means[index].gv += cluster[i].gv;
		means[index].bv += cluster[i].bv;
		means[index].rb += cluster[i].rb;
		means[index].rg += cluster[i].rg;
		means[index].gb += cluster[i].gb;
	}

	for(int i=0; i<means.size(); i++) {
		means[i].x /= cnt[i];
		means[i].y /= cnt[i];
		means[i].rv /= cnt[i];
		means[i].gv /= cnt[i];
		means[i].bv /= cnt[i];
		means[i].rg /= cnt[i];
		means[i].rb /= cnt[i];
		means[i].gb /= cnt[i];
		means[i].label = i;
		KDEBUG(printf("means init: x=%d, y=%d, rv=%d, gv=%d, bv=%d, rg=%f, rb=%f, gb=%f, label=%d\n", means[i].x, means[i].y, means[i].rv, means[i].gv, means[i].bv, means[i].rg, means[i].rb, means[i].gb, means[i].label));	
	}
	return 0;
}

double kmeans_src_calDict(SrcPoint point1, SrcPoint point2) {

	vector<double> tmp1;
	vector<double> tmp2;
//	tmp1.push_back((double)point1.x);
//	tmp1.push_back((double)point1.y);
	tmp1.push_back(point1.rb);
	tmp1.push_back(point1.rg);
	tmp1.push_back(point1.gb);

//	tmp2.push_back((double)point2.x);
//	tmp2.push_back((double)point2.y);
	tmp2.push_back(point2.rb);
	tmp2.push_back(point2.rg);
	tmp2.push_back(point2.gb);

//	tmp1.push_back(point1.x);
//	tmp1.push_back(point1.y);
//	tmp1.push_back(point1.rv);
//	tmp1.push_back(point1.gv);
//	tmp1.push_back(point1.bv);

//	tmp2.push_back(point2.x);
//	tmp2.push_back(point2.y);
//	tmp2.push_back(point2.rv);
//	tmp2.push_back(point2.gv);
//	tmp2.push_back(point2.bv);

	return kmeans_calDict(tmp1, tmp2);
}

int kmeans_src_sort(SrcPoint &point, vector<SrcPoint> &means) {
	double dict = 0;
	double sum = 0;
	dict = kmeans_src_calDict(point, means[0]);
	point.label = 0;
	for(int i=1; i < means.size(); i++) {
		sum = kmeans_src_calDict(point, means[i]);
		if(dict > sum)	{
			dict = sum;
			point.label = i;
		}
	}
	return 0;
}

int kmeans_src_sortCluster(vector<SrcPoint> &means, vector<SrcPoint> &cluster, vector<int> &cnt) {
	cnt.assign(cnt.size(), 0);
	for(int i=0; i < cluster.size(); i++) {
		kmeans_src_sort(cluster[i], means);
		cnt[cluster[i].label] ++;
//		KDEBUG(printf("Sort cluster[%d] label is %d\n", i, cluster[i].label));
	}

	for(int i=0; i<cnt.size(); i++) {
		KDEBUG(printf("Cluster[%d] cnt is %d\n", i, cnt[i]));
	}
	return 0;
}

int kmeans_src_calDeltaSum(vector<SrcPoint> &means, vector<SrcPoint> &cluster, double &sum) {
	int index = 0;
	sum = 0;
	for(int i = 0; i < cluster.size(); i++) {
		index = cluster[i].label;
		sum += kmeans_src_calDict(cluster[i], means[index]);
	}

	//KDEBUG(printf("cluster dict means sum: %f\n", sum));
	return 0;
}

int kmeans_gray_init(vector<GrayPoint> &means, vector<GrayPoint> cluster, int knum) {
	int cnt = 0;
	if((cluster.size() < 2) || (knum < 2)) {
		printf("Kmeans init para error!\n");
		return -1;
	}

	vector<GrayPoint> xcluster;
	xcluster.push_back(cluster[0]);
	for(int i=0; i<cluster.size();i++) {
		if(xcluster[cnt].x != cluster[i].x) {
			xcluster.push_back(cluster[i]);
			cnt ++; 
		} else {
			continue;
		}
		KDEBUG(printf("%d: x = %d, y = %d, v = %d\n", cnt, xcluster[cnt].x, xcluster[cnt].y, xcluster[cnt].v));
	}

	KDEBUG(printf("xcluster size = %d\n", (int)xcluster.size()));
	for(int i=0; i<knum; i++) {
		means.push_back(xcluster[i*((cnt-1)/(knum-1))]);
		means[i].label = i;
		KDEBUG(printf("means init: x=%d, y=%d, v=%d, label=%d\n", means[i].x, means[i].y, means[i].v, means[i].label));			
	}

	return 0;
}

int kmeans_gray_update(vector<GrayPoint> &means, vector<GrayPoint> cluster, vector<int> &cnt) {
	GrayPoint point;
	point.x = 0;
	point.y = 0;
	point.v = 0;
	point.label = 0;
	int index = 0;

	means.assign(means.size(), point);
	for(int i=0; i<cluster.size(); i++) {
		index = cluster[i].label;
		means[index].x += cluster[i].x;
		means[index].y += cluster[i].y;
		means[index].v += cluster[i].v;
	}

	for(int i=0; i<means.size(); i++) {
		means[i].x /= cnt[i];
		means[i].y /= cnt[i];
		means[i].v /= cnt[i];
		means[i].label = i;
		KDEBUG(printf("means update: x=%d, y=%d, v=%d, label=%d\n", means[i].x, means[i].y, means[i].v, means[i].label));
	}
	return 0;
}

int kmeans_gray_calDict(GrayPoint point1, GrayPoint point2) {

	vector<int> tmp1, tmp2;
	tmp1.push_back(point1.x);
	tmp1.push_back(point1.y);
	tmp1.push_back(point1.v);

	tmp2.push_back(point2.x);
	tmp2.push_back(point2.y);
	tmp2.push_back(point2.v);
	return 0;
	//return (int)kmeans_calDict(tmp1, tmp2);
}


int kmeans_gray_sort(GrayPoint &point, vector<GrayPoint> &means) {
	int dict = 0;
	int sum = 0;
	dict = kmeans_gray_calDict(point, means[0]);
	point.label = 0;
	for(int i=1; i < means.size(); i++) {
		sum = kmeans_gray_calDict(point, means[i]);
		if(dict > sum)	{
			dict = sum;
			point.label = i;
		}
	}
	return 0;
}

int kmeans_gray_sortCluster(vector<GrayPoint> &means, vector<GrayPoint> &cluster, vector<int> &cnt) {
	cnt.assign(cnt.size(), 0);
	for(int i=0; i < cluster.size(); i++) {
		kmeans_gray_sort(cluster[i], means);
		cnt[cluster[i].label] ++;
		KDEBUG(printf("Sort cluster[%d] label is %d\n", i, cluster[i].label));
	}

	for(int i=0; i<cnt.size(); i++) {
		KDEBUG(printf("Cluster[%d] cnt is %d\n", i, cnt[i]));
	}
	return 0;
}

int kmeans_gray_calDeltaSum(vector<GrayPoint> &means, vector<GrayPoint> &cluster, long &sum) {
	int index = 0;
	sum = 0;
	for(int i = 0; i < cluster.size(); i++) {
		index = cluster[i].label;
		sum += (long) kmeans_gray_calDict(cluster[i], means[index]);
	}

	KDEBUG(printf("cluster dict means sum: %ld\n", sum));
	return 0;
}
// no use double and sqrt because waste time 
// cal dict sqrt((x1-y1)**(x1-y1) + ... + (xn-yn)**(xn-yn))
static double kmeans_calDict(vector<double> dict1, vector<double> dict2) {
	double sum = 0;
	double temp = 0;

	if ((dict1.size() < 2) || (dict2.size() < 2) || (dict1.size() != dict2.size())) {
		printf("Kmeans cal para error!\n");
		return -1;
	}
	
	for(int i=0; i< dict1.size()-1; i++) {
		temp = dict1[i] - dict2[i];
		sum += temp * temp;
	}

	//KDEBUG(printf("sum = %d\n", sum));
	return sum;
}


int updateGraySubImg(vector<GrayPoint> means, vector<GrayPoint> cluster, Mat mSrc, const char* desPath) {

	int index = 0;
	char cutPath[128] = {0};
	vector<int> xstart(means.size());
	vector<int> xend(means.size());
	Mat roiImg;
	for(int i=0; i<means.size(); i++) {
		xstart[i] = xend[i] = means[i].x;
	}
	for(int i=0; i<cluster.size(); i++) {
		index = cluster[i].label;
		if(xstart[index] > cluster[i].x) {
			xstart[index] = cluster[i].x;
		}
		if(xend[index] < cluster[i].x) {
			xend[index] = cluster[i].x;
		}
	}

	for(int i=0; i<means.size(); i++) {
		KDEBUG(printf("xstart[%d]:%d, xend[%d]:%d\n", i, xstart[i], i, xend[i]));
		memset(cutPath, 0, sizeof(cutPath));
		snprintf(cutPath, sizeof(cutPath), "./%s/cut_%d.png", desPath, i);
		roiImg = mSrc(Range(0, mSrc.rows), Range(xstart[i], xend[i]));
		imwrite(cutPath, roiImg);
	}
	return 0;
}

int updateSrcSubImg(vector<SrcPoint> means, vector<SrcPoint> cluster, Mat mSrc, const char* desPath) {

	int index = 0;
	char cutPath[128] = {0};
	vector<int> xstart(means.size());
	vector<int> xend(means.size());
	Mat roiImg;
	for(int i=0; i<means.size(); i++) {
		xstart[i] = xend[i] = means[i].x;
	}
	for(int i=0; i<cluster.size(); i++) {
		index = cluster[i].label;
		if(xstart[index] > cluster[i].x) {
			xstart[index] = cluster[i].x;
		}
		if(xend[index] < cluster[i].x) {
			xend[index] = cluster[i].x;
		}
	}

	for(int i=0; i<means.size(); i++) {
		KDEBUG(printf("xstart[%d]:%d, xend[%d]:%d\n", i, xstart[i], i, xend[i]));
		memset(cutPath, 0, sizeof(cutPath));
		snprintf(cutPath, sizeof(cutPath), "./%s/cut_%d.png", desPath, i);
		roiImg = mSrc(Range(0, mSrc.rows), Range(xstart[i], xend[i]));
		imwrite(cutPath, roiImg);
	}
	return 0;
}

int updateImg(vector<SrcPoint> means, vector<SrcPoint> cluster, Mat mSrc, const char* desPath) {
	int index = 0;
	Mat roiImg;
	char cutPath[128] = {0};
	for(int k = 0; k<means.size(); k++) {
		mSrc.copyTo(roiImg);
		int cnt = 0;
		for(int i=0; i<cluster.size(); i++) {
			uchar* ptr_m = roiImg.ptr<uchar>(cluster[i].y);
			if(cluster[i].label != k)
				ptr_m[cluster[i].x] = 255;
		}
		
		memset(cutPath, 0, sizeof(cutPath));
		snprintf(cutPath, sizeof(cutPath), "./%s/cut_%d.png", desPath, k);
		imwrite(cutPath, roiImg);
	}
	return 0;
}

int main(int argc, const char* argv[]) {
	Mat mSrc = imread(SRC_IMG, IMREAD_UNCHANGED);
	Mat mGray = imread(SRC_IMG, IMREAD_GRAYSCALE);
	int knum = atoi(KNUM);	
	long gray_sum_old = 0;
	long gray_sum = 0;
	double src_sum_old = 0;
	double src_sum = 0;
	vector<int> gray_cnt(knum, 0);
	vector<int> src_cnt(knum, 0);

	GrayPoint gpoint;
	SrcPoint spoint;
	//init img data
	vector<Mat> mChannels;
	split(mSrc, mChannels);
	Mat mR = mChannels.at(2);
	Mat mG = mChannels.at(1);
	Mat mB = mChannels.at(0);

	for(int i=0; i<mSrc.rows; i++) {
		uchar* ptr_m = mGray.ptr<uchar>(i);
		uchar* ptr_mR = mR.ptr<uchar>(i);
		uchar* ptr_mB = mB.ptr<uchar>(i);
		uchar* ptr_mG = mG.ptr<uchar>(i);
		for(int j=0; j<mSrc.cols; j++) {
			if(ptr_m[j] != 255) {
				gpoint.x = spoint.x = j;
				gpoint.y = spoint.y = i;
				gpoint.v = ptr_m[j];
				spoint.gv = ptr_mG[j];
				spoint.bv = ptr_mB[j];
				spoint.rv = ptr_mR[j];
				gray_cluster.push_back(gpoint);
				src_cluster.push_back(spoint);
			}
		}
	}

	//按x值 冒泡排序
	GrayPoint temp;
	SrcPoint tempSrc;
	for(int i=0; i<gray_cluster.size(); i++) {
		for(int j=0; j<gray_cluster.size()-i-1; j++) {
			if(gray_cluster[j].x > gray_cluster[j+1].x) {
				temp = gray_cluster[j];
				gray_cluster[j] = gray_cluster[j+1];
				gray_cluster[j+1] = temp;
				tempSrc = src_cluster[j];
				src_cluster[j] = src_cluster[j+1];
				src_cluster[j+1] = tempSrc;
			}		
		}
	}

#if 0
	kmeans_gray_init(gray_means, gray_cluster, knum);
	kmeans_gray_sortCluster(gray_means, gray_cluster, gray_cnt);
	kmeans_gray_calDeltaSum(gray_means, gray_cluster, gray_sum);
	while(abs(gray_sum - gray_sum_old) > 1) {
		gray_sum_old = gray_sum;
		kmeans_gray_update(gray_means, gray_cluster, gray_cnt);
		kmeans_gray_sortCluster(gray_means, gray_cluster, gray_cnt);
		kmeans_gray_calDeltaSum(gray_means, gray_cluster, gray_sum);
		KDEBUG(printf("gray_sum is %ld, gray_sum_old is %ld\n", gray_sum, gray_sum_old));
	}
	updateGraySubImg(gray_means, gray_cluster, mSrc, DES_IMG);
#endif
#if 1
	kmeans_src_init(src_means, src_cluster, knum);
	kmeans_src_sortCluster(src_means, src_cluster, src_cnt);
	kmeans_src_calDeltaSum(src_means, src_cluster, src_sum);
	while(abs(src_sum - src_sum_old) > 0.0001) {
		src_sum_old = src_sum;
		kmeans_src_update(src_means, src_cluster, src_cnt);
		kmeans_src_sortCluster(src_means, src_cluster, src_cnt);
		kmeans_src_calDeltaSum(src_means, src_cluster, src_sum);
		KDEBUG(printf("src_sum is %f, src_sum_old is %f\n", src_sum, src_sum_old));
	}
	//updateSrcSubImg(src_means, src_cluster, mSrc, DES_IMG);
	updateImg(src_means, src_cluster, mGray, DES_IMG);
#endif
	//imshow("SrcImg", mSrc);
	//imshow("GrayImg", mGray);
	waitKey(0);
	return 0;
}
