#include <efi.h>
#include <efilib.h>

EFI_STATUS
efi_main(EFI_HANDLE image, EFI_SYSTEM_TABLE *systab) {
  SIMPLE_TEXT_OUTPUT_INTERFACE *conout;

  conout = systab->ConOut;
  InitializeLib(image, systab);
  int x=(int)conout->Mode;
  //uefi_call_wrapper(conout->OutputString, 2, conout, L"Hello World!\n\r");

  return EFI_SUCCESS;
}
