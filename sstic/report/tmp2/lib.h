#pragma once
#include "Ddraw.h"
#include "test_Export.h"

test_EXPORT void test();


HRESULT WINAPI DirectDrawCreate(
	_In_  GUID FAR         *lpGUID,
	_Out_ LPDIRECTDRAW FAR *lplpDD,
	_In_  IUnknown FAR     *pUnkOuter
	);