#include <dlfcn.h>
#include <cstdio>

typedef void *(*real_malloc_t)(size_t);
static real_malloc_t real_malloc = nullptr;

void init_x() {
  if (real_malloc == nullptr) {
    real_malloc = (real_malloc_t)dlsym(RTLD_NEXT, "malloc");
  }
}

extern "C" void *malloc(int len) {
  init_x();
  void *res = real_malloc(len);
  fprintf(stderr, "abc %p %p\n", res, (char*)res+len);
  return res;
}
