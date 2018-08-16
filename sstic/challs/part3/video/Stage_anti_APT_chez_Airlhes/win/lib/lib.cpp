#include "lib.h"
#include "test_Export.h"
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include "WinBase.h"
#include "lodepng.h"
#include <cassert>
#include <string>

#include <ntddkbd.h>
#include <ntddk.h>

int a = IRP_MJ_WRITE;
int x = UserMode;


using namespace std;
ofstream log_file("log.out", std::ofstream::binary);

const int w = 1280;
const int h = 720;
char surface_buf[w*h * 3];

test_EXPORT void test(){
  printf("bonjour\n");
}
void WINAPI GetLocalTime(_Out_ LPSYSTEMTIME lpSystemTime){
  log_file << " FUUU" << flush;
  exit(0);

}


DDPIXELFORMAT g_pixel_fmt;

class MyDirectDrawSurface : public IDirectDrawSurface
{
  public:
    /*** IUnknown methods ***/
    STDMETHOD(QueryInterface) (THIS_ REFIID riid, LPVOID FAR * ppvObj) { log_file << "DirectDrawSurface QueryInterface XX \n" << flush; return 0; }
    STDMETHOD_(ULONG, AddRef) (THIS){ log_file << "DirectDrawSurface KXX" << flush; return 0; }
    STDMETHOD_(ULONG, Release) (THIS){ log_file << "DirectDrawSurface KXX" << flush; return 0; }
    /*** IDirectDrawSurface methods ***/
    STDMETHOD(AddAttachedSurface)(THIS_ LPDIRECTDRAWSURFACE) { log_file << "DirectDrawSurface AddAttachedSurface XX \n" << flush; return 0; }
    STDMETHOD(AddOverlayDirtyRect)(THIS_ LPRECT) { log_file << "DirectDrawSurface AddOverlayDirtyRect XX \n" << flush; return 0; }
    STDMETHOD(Blt)(THIS_ LPRECT, LPDIRECTDRAWSURFACE, LPRECT, DWORD, LPDDBLTFX) { log_file << "DirectDrawSurface Blt XX \n" << flush; return 0; }
    STDMETHOD(BltBatch)(THIS_ LPDDBLTBATCH, DWORD, DWORD) { log_file << "DirectDrawSurface BltBatch XX \n" << flush; return 0; }
    STDMETHOD(BltFast)(THIS_ DWORD, DWORD, LPDIRECTDRAWSURFACE, LPRECT, DWORD) { log_file << "DirectDrawSurface BltFast XX \n" << flush; return 0; }
    STDMETHOD(DeleteAttachedSurface)(THIS_ DWORD, LPDIRECTDRAWSURFACE) { log_file << "DirectDrawSurface DeleteAttachedSurface XX \n" << flush; return 0; }
    STDMETHOD(EnumAttachedSurfaces)(THIS_ LPVOID, LPDDENUMSURFACESCALLBACK) { log_file << "DirectDrawSurface EnumAttachedSurfaces XX \n" << flush; return 0; }
    STDMETHOD(EnumOverlayZOrders)(THIS_ DWORD, LPVOID, LPDDENUMSURFACESCALLBACK) { log_file << "DirectDrawSurface EnumOverlayZOrders XX \n" << flush; return 0; }
    STDMETHOD(Flip)(THIS_ LPDIRECTDRAWSURFACE, DWORD) {
      if (0){
        typedef int(*checkit)();
        checkit t1 = (checkit)(0x403750);
        SYSTEMTIME time;
        GetSystemTime(&time);

        for (int t = 0; t < 24 * 60 * 60; ++t){
          int curt = t;
          time.wSecond = curt % 60;
          curt /= 60;
          time.wMinute = curt % 60;
          curt /= 60;
          time.wHour = curt;

          //SetSystemTime(&time);
          int res = t1();
          char buf[200];
          sprintf(buf, "res >> %02d:%02d:%02d >> %d", time.wHour, time.wMinute, time.wSecond, res);
          Sleep(1);

        }
        exit(0);
      }
      do_dump();
      log_file << "DirectDrawSurface Flip XX \n" << flush; return 0;
    }
    STDMETHOD(GetAttachedSurface)(THIS_ LPDDSCAPS, LPDIRECTDRAWSURFACE FAR * out_surf) { *out_surf = this; log_file << "DirectDrawSurface GetAttachedSurface XX \n" << flush; return 0; }
    STDMETHOD(GetBltStatus)(THIS_ DWORD) { log_file << "DirectDrawSurface GetBltStatus XX \n" << flush; return 0; }
    STDMETHOD(GetCaps)(THIS_ LPDDSCAPS) { log_file << "DirectDrawSurface GetCaps XX \n" << flush; return 0; }
    STDMETHOD(GetClipper)(THIS_ LPDIRECTDRAWCLIPPER FAR*) { log_file << "DirectDrawSurface GetClipper XX \n" << flush; return 0; }
    STDMETHOD(GetColorKey)(THIS_ DWORD, LPDDCOLORKEY) { log_file << "DirectDrawSurface GetColorKey XX \n" << flush; return 0; }
    STDMETHOD(GetDC)(THIS_ HDC FAR *) { log_file << "DirectDrawSurface GetDC XX \n" << flush; return 0; }
    STDMETHOD(GetFlipStatus)(THIS_ DWORD) { log_file << "DirectDrawSurface GetFlipStatus XX \n" << flush; return 0; }
    STDMETHOD(GetOverlayPosition)(THIS_ LPLONG, LPLONG) { log_file << "DirectDrawSurface GetOverlayPosition XX \n" << flush; return 0; }
    STDMETHOD(GetPalette)(THIS_ LPDIRECTDRAWPALETTE FAR*) { log_file << "DirectDrawSurface GetPalette XX \n" << flush; return 0; }
    STDMETHOD(GetPixelFormat)(THIS_ LPDDPIXELFORMAT out_fmt) {
      log_file << "DirectDrawSurface GetPixelFormat XX \n" << flush;
      out_fmt->dwSize = 3;
      out_fmt->dwFlags = 0x40; //required, DD_RGB
      out_fmt->dwFourCC = 0x789;
      out_fmt->dwRGBBitCount = 24;
      out_fmt->dwRBitMask = 0xff;
      out_fmt->dwGBitMask = 0xff00;
      out_fmt->dwBBitMask = 0xff0000;



      return 0;
    }
    STDMETHOD(GetSurfaceDesc)(THIS_ LPDDSURFACEDESC) { log_file << "DirectDrawSurface GetSurfaceDesc XX \n" << flush; return 0; }
    STDMETHOD(Initialize)(THIS_ LPDIRECTDRAW, LPDDSURFACEDESC) { log_file << "DirectDrawSurface Initialize XX \n" << flush; return 0; }
    STDMETHOD(IsLost)(THIS){ log_file << "DirectDrawSurface IsLost XX \n" << flush; return 0; }
    STDMETHOD(Lock)(THIS_ LPRECT, LPDDSURFACEDESC io_surf, DWORD, HANDLE) {
      io_surf->lPitch = w * 3;
      io_surf->lpSurface = surface_buf;
      io_surf->dwWidth = w;
      io_surf->dwHeight = h;
      log_file << "DirectDrawSurface Lock XX \n" << flush; return 0;
    }
    STDMETHOD(ReleaseDC)(THIS_ HDC) { log_file << "DirectDrawSurface ReleaseDC XX \n" << flush; return 0; }
    STDMETHOD(Restore)(THIS){ log_file << "DirectDrawSurface Restore XX \n" << flush; return 0; }
    STDMETHOD(SetClipper)(THIS_ LPDIRECTDRAWCLIPPER) { log_file << "DirectDrawSurface SetClipper XX \n" << flush; return 0; }
    STDMETHOD(SetColorKey)(THIS_ DWORD, LPDDCOLORKEY) { log_file << "DirectDrawSurface SetColorKey XX \n" << flush; return 0; }
    STDMETHOD(SetOverlayPosition)(THIS_ LONG, LONG) { log_file << "DirectDrawSurface SetOverlayPosition XX \n" << flush; return 0; }
    STDMETHOD(SetPalette)(THIS_ LPDIRECTDRAWPALETTE) { log_file << "DirectDrawSurface SetPalette XX \n" << flush; return 0; }
    STDMETHOD(Unlock)(THIS_ LPVOID) { log_file << "DirectDrawSurface Unlock XX \n" << flush; return 0; }
    STDMETHOD(UpdateOverlay)(THIS_ LPRECT, LPDIRECTDRAWSURFACE, LPRECT, DWORD, LPDDOVERLAYFX) { log_file << "DirectDrawSurface UpdateOverlay XX \n" << flush; return 0; }
    STDMETHOD(UpdateOverlayDisplay)(THIS_ DWORD) { log_file << "DirectDrawSurface UpdateOverlayDisplay XX \n" << flush; return 0; }
    STDMETHOD(UpdateOverlayZOrder)(THIS_ DWORD, LPDIRECTDRAWSURFACE) { log_file << "DirectDrawSurface UpdateOverlayZOrder XX \n" << flush; return 0; }

  private:
    void do_dump(){
      char filename[200];
      if (blit_count % 1 == 0){
        sprintf(filename, "out/res_%04d.png", blit_count);
        unsigned int err = lodepng::encode(string(filename), (const unsigned char*)surface_buf, w, h, LodePNGColorType::LCT_RGB);
        assert(err == 0);
      }
      blit_count += 1;
      if (blit_count == 400)
        exit(0);


    }
    int blit_count = 0;
};

MyDirectDrawSurface g_surface;

class MyDirectDraw : public IDirectDraw {
  public:
    STDMETHOD(QueryInterface) (THIS_ REFIID riid, LPVOID FAR * ppvObj) { log_file << "On QueryInterface\n" << flush; return 0; }
    STDMETHOD_(ULONG, AddRef) (THIS){ log_file << "AddRef\n" << flush; return 0; }
    STDMETHOD_(ULONG, Release) (THIS){ log_file << "AddRef\n" << flush; return 0; }
    /*** IDirectDraw methods ***/
    STDMETHOD(Compact)(THIS){ log_file << "Compact\n" << flush; return 0; }
    STDMETHOD(CreateClipper)(THIS_ DWORD, LPDIRECTDRAWCLIPPER FAR*, IUnknown FAR *) { log_file << "CreateClipper\n" << flush; return 0; }
    STDMETHOD(CreatePalette)(THIS_ DWORD, LPPALETTEENTRY, LPDIRECTDRAWPALETTE FAR*, IUnknown FAR *) { log_file << "CreatePalette\n" << flush; return 0; }
    STDMETHOD(CreateSurface)(THIS_  LPDDSURFACEDESC desc, LPDIRECTDRAWSURFACE FAR *surface, IUnknown FAR *) { log_file << "CreateSurface" <<  desc->dwWidth << ' ' << desc->dwHeight << ' '<< desc->lPitch << ' ' << desc->ddpfPixelFormat.dwRGBBitCount << "\n" <<flush; *surface = &g_surface; return 0; }
    STDMETHOD(DuplicateSurface)(THIS_ LPDIRECTDRAWSURFACE, LPDIRECTDRAWSURFACE FAR *) { log_file << "DuplicateSurface\n" << flush; return 0; }
    STDMETHOD(EnumDisplayModes)(THIS_ DWORD, LPDDSURFACEDESC, LPVOID, LPDDENUMMODESCALLBACK) { log_file << "EnumDisplayModes\n" << flush; return 0; }
    STDMETHOD(EnumSurfaces)(THIS_ DWORD, LPDDSURFACEDESC, LPVOID, LPDDENUMSURFACESCALLBACK) { log_file << "EnumSurfaces\n" << flush; return 0; }
    STDMETHOD(FlipToGDISurface)(THIS){ log_file << "FlipToGDISurface\n" << flush; return 0; }
    STDMETHOD(GetCaps)(THIS_ LPDDCAPS, LPDDCAPS) { log_file << "GetCaps\n" << flush; return 0; }
    STDMETHOD(GetDisplayMode)(THIS_ LPDDSURFACEDESC) { log_file << "GetDisplayMode\n" << flush; return 0; }
    STDMETHOD(GetFourCCCodes)(THIS_  LPDWORD, LPDWORD) { log_file << "GetFourCCCodes\n" << flush; return 0; }
    STDMETHOD(GetGDISurface)(THIS_ LPDIRECTDRAWSURFACE FAR *) { log_file << "GetGDISurface\n" << flush; return 0; }
    STDMETHOD(GetMonitorFrequency)(THIS_ LPDWORD) { log_file << "GetMonitorFrequency\n" << flush; return 0; }
    STDMETHOD(GetScanLine)(THIS_ LPDWORD) { log_file << "GetScanLine\n" << flush; return 0; }
    STDMETHOD(GetVerticalBlankStatus)(THIS_ LPBOOL) { log_file << "GetVertiacalBlankStatus\n" << flush; return 0; }
    STDMETHOD(Initialize)(THIS_ GUID FAR *) { log_file << "Initialize\n" << flush; return 0; }
    STDMETHOD(RestoreDisplayMode)(THIS){ log_file << "RestoreDisplayMode\n" << flush; return 0; }
    STDMETHOD(SetCooperativeLevel)(THIS_ HWND, DWORD) { log_file << "SetCooperativeLevel\n" << flush; return 0; }
    STDMETHOD(SetDisplayMode)(THIS_ DWORD, DWORD, DWORD) { log_file << "SetDisplayMode\n" << flush; return 0; }
    STDMETHOD(WaitForVerticalBlank)(THIS_ DWORD, HANDLE) { log_file << "WaitForVerticalBlank\n" << flush; return 0; }
};

MyDirectDraw g_draw;

HRESULT WINAPI DirectDrawCreate(
    _In_  GUID FAR         *lpGUID,
    _Out_ LPDIRECTDRAW FAR *lplpDD,
    _In_  IUnknown FAR     *pUnkOuter
    ){
  log_file << "KAPPA";
  log_file.flush();
  *lplpDD = &g_draw;
  int *is_activate = (int*)0x0040F0E0;
  *is_activate = 1;


  return 0;
}
