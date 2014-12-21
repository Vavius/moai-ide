#include <iostream>
#include <string>
#include <moai-core/host.h>

using namespace std;

int main() {
    cout << "Hello world!" << endl;
    AKUAppInitialize();
    AKUModulesAppInitialize ();
    int ctx = AKUCreateContext();
    cout << ctx << endl;
    return 0;
}
