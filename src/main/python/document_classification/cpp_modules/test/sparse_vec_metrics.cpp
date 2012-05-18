
#include "../sparse_vec_metrics.hpp"

int main() {
	IntDoubleListPairs v1;
	v1.push_back( make_pair<int, double>(1,2.0) );
	printPairVector("v1=",v1);

	IntDoubleListPairs v2;
	v2.push_back( make_pair<int, double>(1,2.0) );
	v2.push_back( make_pair<int, double>(2,4.0) );
	printPairVector("v2=",v2);

	IntDoubleListPairs v3;
	v3.push_back( make_pair<int, double>(10,2.0) );
	v3.push_back( make_pair<int, double>(20,4.0) );
	v3.push_back( make_pair<int, double>(30,6.0) );
	printPairVector("v3=",v3);

	IntDoubleListPairs v4;
	v4.push_back( make_pair<int, double>(15,2.0) );
	v4.push_back( make_pair<int, double>(20,4.0) );
	v4.push_back( make_pair<int, double>(35,6.0) );
	printPairVector("v4=",v4);

	IntDoubleListPairs v5;
	v5.push_back( make_pair<int, double>(15,2.0) );
	v5.push_back( make_pair<int, double>(35,4.0) );
	v5.push_back( make_pair<int, double>(40,8.0) );
	v5.push_back( make_pair<int, double>(50,10.0) );
	printPairVector("v5=",v5);

	IntDoubleListPairs v6;
	v6.push_back( make_pair<int, double>(5,4.0) );
	v6.push_back( make_pair<int, double>(15,2.0) );
	v6.push_back( make_pair<int, double>(40,8.0) );
	v6.push_back( make_pair<int, double>(55,10.0) );
	printPairVector("v6=",v6);

	cout<<"tversky(v1,v2)="<<tversky(v1,v2)<<" and should be 0.5"<<endl;
	cout<<"tversky(v2,v1)="<<tversky(v2,v1)<<" and should be 0.5"<<endl;

	cout<<"tversky(v3,v2)="<<tversky(v3,v2)<<" and should be 0.0"<<endl;
	cout<<"tversky(v2,v3)="<<tversky(v2,v3)<<" and should be 0.0"<<endl;

	cout<<"tversky(v3,v4)="<<tversky(v3,v4)<<" and should be 0.2"<<endl;
	cout<<"tversky(v4,v3)="<<tversky(v4,v3)<<" and should be 0.2"<<endl;

	cout<<"tversky(v5,v4)="<<tversky(v5,v4)<<" and should be 0.4"<<endl;
	cout<<"tversky(v4,v5)="<<tversky(v4,v5)<<" and should be 0.4"<<endl;

	cout<<"tversky(v6,v5)="<<tversky(v6,v5)<<" and should be 0.3333"<<endl;
	cout<<"tversky(v5,v6)="<<tversky(v5,v6)<<" and should be 0.3333"<<endl;

	cout<<"mul(v1,v1)="<<(mul(v1,v1))<<" and should be "<<(4.0)<<endl;
	cout<<"mul(v2,v2)="<<(mul(v2,v2))<<" and should be "<<(20.0)<<endl;

	cout<<"mul(v1,v2)="<<(mul(v1,v2))<<" and should be "<<(4.0)<<endl;
	cout<<"mul(v2,v1)="<<(mul(v2,v1))<<" and should be "<<(4.0)<<endl;

	cout<<"mul(v3,v4)="<<(mul(v3,v4))<<" and should be "<<(16.0)<<endl;
	cout<<"mul(v4,v3)="<<(mul(v4,v3))<<" and should be "<<(16.0)<<endl;

	cout<<"mul(v3,v5)="<<(mul(v3,v5))<<" and should be "<<(0.0)<<endl;
	cout<<"mul(v5,v3)="<<(mul(v5,v3))<<" and should be "<<(0.0)<<endl;

	cout<<"mul(v4,v5)="<<(mul(v4,v5))<<" and should be "<<(28.0)<<endl;
	cout<<"mul(v5,v4)="<<(mul(v5,v4))<<" and should be "<<(28.0)<<endl;

	cout<<"mul(v6,v5)="<<(mul(v6,v5))<<" and should be "<<(68.0)<<endl;
	cout<<"mul(v5,v6)="<<(mul(v5,v6))<<" and should be "<<(68.0)<<endl;

	cout<<"mul(v5,v5)="<<(mul(v5,v5))<<" and should be "<<(184.0)<<endl;
	cout<<"mul(v6,v6)="<<(mul(v6,v6))<<" and should be "<<(184.0)<<endl;
}
