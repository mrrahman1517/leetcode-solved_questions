#include <iostream>
#include <queue>
#include <vector>
using namespace std;

class MedianFinder {
public:
    priority_queue<int, vector<int>, less<int> > small; // max heap
    priority_queue<int, vector<int>, greater<int> > large;  // min heap
    MedianFinder() {
        
    }
    
    void addNum(int num) {
        small.push(num);
        if(small.size() > large.size()) {
            large.push(small.top());
            small.pop();
        }
        if (small.top() > large.top()) {
            large.push(small.top());
            small.pop();
            small.push(large.top());
            large.pop();
        }
    }
    
    double findMedian() {
        if (small.size() == large.size()) {
            return (double) (small.top() + large.top()) / 2.0;
        }
        else {
            return large.top();
        }
    }
};

int main() {
    MedianFinder* obj = new MedianFinder();
    obj->addNum(1);
    obj->addNum(2);
    cout << obj->findMedian() << endl;
    obj->addNum(3);
    cout << obj->findMedian() << endl;
    return 0;
}