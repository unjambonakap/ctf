; ---------------------------------------------------------------------------

GUID		struc ;	(sizeof=0x10, align=0x4, copyof_1)
					; XREF:	.rdata:00000001400062C4/r
Data1		dd ?
Data2		dw ?
Data3		dw ?
Data4		db 8 dup(?)
GUID		ends

; ---------------------------------------------------------------------------

UNICODE_STRING	struc ;	(sizeof=0x10, align=0x8, copyof_3) ; XREF: get_routine_address/r
Length		dw ?
MaximumLength	dw ?
		db ? ; undefined
		db ? ; undefined
		db ? ; undefined
		db ? ; undefined
Buffer		dq ?			; offset
UNICODE_STRING	ends

; ---------------------------------------------------------------------------

RTL_BITMAP	struc ;	(sizeof=0x10, align=0x8, copyof_9) ; XREF: sub_14000B82C/r
					; sub_14000B82C/r ...
SizeOfBitMap	dd ?
		db ? ; undefined
		db ? ; undefined
		db ? ; undefined
		db ? ; undefined
Buffer		dq ?			; offset
RTL_BITMAP	ends

; ---------------------------------------------------------------------------

RUNTIME_FUNCTION struc ; (sizeof=0xC, mappedto_15) ; XREF: .pdata:ExceptionDir/r
					; .pdata:000000014000A00C/r ...
FunctionStart	dd ?			; offset rva
FunctionEnd	dd ?			; offset rva pastend
UnwindInfo	dd ?			; offset rva
RUNTIME_FUNCTION ends

; ---------------------------------------------------------------------------

UNWIND_INFO	struc ;	(sizeof=0x4, mappedto_16) ; XREF: .rdata:stru_140006558/r
					; .rdata:stru_140006580/r ...
Ver3_Flags	db ?			; base 16
PrologSize	db ?			; base 16
CntUnwindCodes	db ?			; base 16
FrReg_FrRegOff	db ?			; base 16
UNWIND_INFO	ends

; ---------------------------------------------------------------------------

UNWIND_CODE	struc ;	(sizeof=0x2, mappedto_17) ; XREF: .rdata:000000014000655C/r
					; .rdata:000000014000655E/r ...
PrologOff	db ?			; base 16
OpCode_OpInfo	db ?			; base 16
UNWIND_CODE	ends

; ---------------------------------------------------------------------------

C_SCOPE_TABLE	struc ;	(sizeof=0x10, mappedto_18) ; XREF: .rdata:0000000140006570/r
					; .rdata:00000001400067BC/r ...
Begin		dd ?			; offset rva
End		dd ?			; offset rva pastend
Handler		dd ?			; offset rva
Target		dd ?			; offset rva
C_SCOPE_TABLE	ends

; ---------------------------------------------------------------------------

_msEhRef	struc ;	(sizeof=0x20, mappedto_19)
Id		dd ?			; base 16
Cnt1		dd ?			; base 10
Tbl1		dd ?			; offset rva
Cnt2		dd ?			; base 10
Tbl2		dd ?			; offset rva
Cnt3		dd ?			; base 10
Tbl3		dd ?			; offset rva
_unk		dd ?			; base 16
_msEhRef	ends

; ---------------------------------------------------------------------------

_msEhDsc1	struc ;	(sizeof=0x8, mappedto_20)
Mode		dd ?			; base 10
Entry		dd ?			; offset rva
_msEhDsc1	ends

; ---------------------------------------------------------------------------

_msEhDsc2	struc ;	(sizeof=0x8, mappedto_21)
Entry		dd ?			; offset rva
Mode		dd ?			; base 10
_msEhDsc2	ends

; ---------------------------------------------------------------------------

WDFFUNCTIONS	struc ;	(sizeof=0xD80, mappedto_29)
pfnWdfChildListCreate dq ?
pfnWdfChildListGetDevice dq ?
pfnWdfChildListRetrievePdo dq ?
pfnWdfChildListRetrieveAddressDescription dq ?
pfnWdfChildListBeginScan dq ?
pfnWdfChildListEndScan dq ?
pfnWdfChildListBeginIteration dq ?
pfnWdfChildListRetrieveNextDevice dq ?
pfnWdfChildListEndIteration dq ?
pfnWdfChildListAddOrUpdateChildDescriptionAsPresent dq ?
pfnWdfChildListUpdateChildDescriptionAsMissing dq ?
pfnWdfChildListUpdateAllChildDescriptionsAsPresent dq ?
pfnWdfChildListRequestChildEject dq ?
pfnWdfCollectionCreate dq ?
pfnWdfCollectionGetCount dq ?
pfnWdfCollectionAdd dq ?
pfnWdfCollectionRemove dq ?
pfnWdfCollectionRemoveItem dq ?
pfnWdfCollectionGetItem	dq ?
pfnWdfCollectionGetFirstItem dq	?
pfnWdfCollectionGetLastItem dq ?
pfnWdfCommonBufferCreate dq ?
pfnWdfCommonBufferGetAlignedVirtualAddress dq ?
pfnWdfCommonBufferGetAlignedLogicalAddress dq ?
pfnWdfCommonBufferGetLength dq ?
pfnWdfControlDeviceInitAllocate	dq ?
pfnWdfControlDeviceInitSetShutdownNotification dq ?
pfnWdfControlFinishInitializing	dq ?
pfnWdfDeviceGetDeviceState dq ?
pfnWdfDeviceSetDeviceState dq ?
pfnWdfWdmDeviceGetWdfDeviceHandle dq ?
pfnWdfDeviceWdmGetDeviceObject dq ?
pfnWdfDeviceWdmGetAttachedDevice dq ?
pfnWdfDeviceWdmGetPhysicalDevice dq ?
pfnWdfDeviceWdmDispatchPreprocessedIrp dq ?
pfnWdfDeviceAddDependentUsageDeviceObject dq ?
pfnWdfDeviceAddRemovalRelationsPhysicalDevice dq ?
pfnWdfDeviceRemoveRemovalRelationsPhysicalDevice dq ?
pfnWdfDeviceClearRemovalRelationsDevices dq ?
pfnWdfDeviceGetDriver dq ?
pfnWdfDeviceRetrieveDeviceName dq ?
pfnWdfDeviceAssignMofResourceName dq ?
pfnWdfDeviceGetIoTarget	dq ?
pfnWdfDeviceGetDevicePnpState dq ?
pfnWdfDeviceGetDevicePowerState	dq ?
pfnWdfDeviceGetDevicePowerPolicyState dq ?
pfnWdfDeviceAssignS0IdleSettings dq ?
pfnWdfDeviceAssignSxWakeSettings dq ?
pfnWdfDeviceOpenRegistryKey dq ?
pfnWdfDeviceSetSpecialFileSupport dq ?
pfnWdfDeviceSetCharacteristics dq ?
pfnWdfDeviceGetCharacteristics dq ?
pfnWdfDeviceGetAlignmentRequirement dq ?
pfnWdfDeviceSetAlignmentRequirement dq ?
pfnWdfDeviceInitFree dq	?
pfnWdfDeviceInitSetPnpPowerEventCallbacks dq ?
pfnWdfDeviceInitSetPowerPolicyEventCallbacks dq	?
pfnWdfDeviceInitSetPowerPolicyOwnership	dq ?
pfnWdfDeviceInitRegisterPnpStateChangeCallback dq ?
pfnWdfDeviceInitRegisterPowerStateChangeCallback dq ?
pfnWdfDeviceInitRegisterPowerPolicyStateChangeCallback dq ?
pfnWdfDeviceInitSetIoType dq ?
pfnWdfDeviceInitSetExclusive dq	?
pfnWdfDeviceInitSetPowerNotPageable dq ?
pfnWdfDeviceInitSetPowerPageable dq ?
pfnWdfDeviceInitSetPowerInrush dq ?
pfnWdfDeviceInitSetDeviceType dq ?
pfnWdfDeviceInitAssignName dq ?
pfnWdfDeviceInitAssignSDDLString dq ?
pfnWdfDeviceInitSetDeviceClass dq ?
pfnWdfDeviceInitSetCharacteristics dq ?
pfnWdfDeviceInitSetFileObjectConfig dq ?
pfnWdfDeviceInitSetRequestAttributes dq	?
pfnWdfDeviceInitAssignWdmIrpPreprocessCallback dq ?
pfnWdfDeviceInitSetIoInCallerContextCallback dq	?
pfnWdfDeviceCreate dq ?
pfnWdfDeviceSetStaticStopRemove	dq ?
pfnWdfDeviceCreateDeviceInterface dq ?
pfnWdfDeviceSetDeviceInterfaceState dq ?
pfnWdfDeviceRetrieveDeviceInterfaceString dq ?
pfnWdfDeviceCreateSymbolicLink dq ?
pfnWdfDeviceQueryProperty dq ?
pfnWdfDeviceAllocAndQueryProperty dq ?
pfnWdfDeviceSetPnpCapabilities dq ?
pfnWdfDeviceSetPowerCapabilities dq ?
pfnWdfDeviceSetBusInformationForChildren dq ?
pfnWdfDeviceIndicateWakeStatus dq ?
pfnWdfDeviceSetFailed dq ?
pfnWdfDeviceStopIdle dq	?
pfnWdfDeviceResumeIdle dq ?
pfnWdfDeviceGetFileObject dq ?
pfnWdfDeviceEnqueueRequest dq ?
pfnWdfDeviceGetDefaultQueue dq ?
pfnWdfDeviceConfigureRequestDispatching	dq ?
pfnWdfDmaEnablerCreate dq ?
pfnWdfDmaEnablerGetMaximumLength dq ?
pfnWdfDmaEnablerGetMaximumScatterGatherElements	dq ?
pfnWdfDmaEnablerSetMaximumScatterGatherElements	dq ?
pfnWdfDmaTransactionCreate dq ?
pfnWdfDmaTransactionInitialize dq ?
pfnWdfDmaTransactionInitializeUsingRequest dq ?
pfnWdfDmaTransactionExecute dq ?
pfnWdfDmaTransactionRelease dq ?
pfnWdfDmaTransactionDmaCompleted dq ?
pfnWdfDmaTransactionDmaCompletedWithLength dq ?
pfnWdfDmaTransactionDmaCompletedFinal dq ?
pfnWdfDmaTransactionGetBytesTransferred	dq ?
pfnWdfDmaTransactionSetMaximumLength dq	?
pfnWdfDmaTransactionGetRequest dq ?
pfnWdfDmaTransactionGetCurrentDmaTransferLength	dq ?
pfnWdfDmaTransactionGetDevice dq ?
pfnWdfDpcCreate	dq ?
pfnWdfDpcEnqueue dq ?
pfnWdfDpcCancel	dq ?
pfnWdfDpcGetParentObject dq ?
pfnWdfDpcWdmGetDpc dq ?
pfnWdfDriverCreate dq ?
pfnWdfDriverGetRegistryPath dq ?
pfnWdfDriverWdmGetDriverObject dq ?
pfnWdfDriverOpenParametersRegistryKey dq ?
pfnWdfWdmDriverGetWdfDriverHandle dq ?
pfnWdfDriverRegisterTraceInfo dq ?
pfnWdfDriverRetrieveVersionString dq ?
pfnWdfDriverIsVersionAvailable dq ?
pfnWdfFdoInitWdmGetPhysicalDevice dq ?
pfnWdfFdoInitOpenRegistryKey dq	?
pfnWdfFdoInitQueryProperty dq ?
pfnWdfFdoInitAllocAndQueryProperty dq ?
pfnWdfFdoInitSetEventCallbacks dq ?
pfnWdfFdoInitSetFilter dq ?
pfnWdfFdoInitSetDefaultChildListConfig dq ?
pfnWdfFdoQueryForInterface dq ?
pfnWdfFdoGetDefaultChildList dq	?
pfnWdfFdoAddStaticChild	dq ?
pfnWdfFdoLockStaticChildListForIteration dq ?
pfnWdfFdoRetrieveNextStaticChild dq ?
pfnWdfFdoUnlockStaticChildListFromIteration dq ?
pfnWdfFileObjectGetFileName dq ?
pfnWdfFileObjectGetFlags dq ?
pfnWdfFileObjectGetDevice dq ?
pfnWdfFileObjectWdmGetFileObject dq ?
pfnWdfInterruptCreate dq ?
pfnWdfInterruptQueueDpcForIsr dq ?
pfnWdfInterruptSynchronize dq ?
pfnWdfInterruptAcquireLock dq ?
pfnWdfInterruptReleaseLock dq ?
pfnWdfInterruptEnable dq ?
pfnWdfInterruptDisable dq ?
pfnWdfInterruptWdmGetInterrupt dq ?
pfnWdfInterruptGetInfo dq ?
pfnWdfInterruptSetPolicy dq ?
pfnWdfInterruptGetDevice dq ?
pfnWdfIoQueueCreate dq ?
pfnWdfIoQueueGetState dq ?
pfnWdfIoQueueStart dq ?
pfnWdfIoQueueStop dq ?
pfnWdfIoQueueStopSynchronously dq ?
pfnWdfIoQueueGetDevice dq ?
pfnWdfIoQueueRetrieveNextRequest dq ?
pfnWdfIoQueueRetrieveRequestByFileObject dq ?
pfnWdfIoQueueFindRequest dq ?
pfnWdfIoQueueRetrieveFoundRequest dq ?
pfnWdfIoQueueDrainSynchronously	dq ?
pfnWdfIoQueueDrain dq ?
pfnWdfIoQueuePurgeSynchronously	dq ?
pfnWdfIoQueuePurge dq ?
pfnWdfIoQueueReadyNotify dq ?
pfnWdfIoTargetCreate dq	?
pfnWdfIoTargetOpen dq ?
pfnWdfIoTargetCloseForQueryRemove dq ?
pfnWdfIoTargetClose dq ?
pfnWdfIoTargetStart dq ?
pfnWdfIoTargetStop dq ?
pfnWdfIoTargetGetState dq ?
pfnWdfIoTargetGetDevice	dq ?
pfnWdfIoTargetQueryTargetProperty dq ?
pfnWdfIoTargetAllocAndQueryTargetProperty dq ?
pfnWdfIoTargetQueryForInterface	dq ?
pfnWdfIoTargetWdmGetTargetDeviceObject dq ?
pfnWdfIoTargetWdmGetTargetPhysicalDevice dq ?
pfnWdfIoTargetWdmGetTargetFileObject dq	?
pfnWdfIoTargetWdmGetTargetFileHandle dq	?
pfnWdfIoTargetSendReadSynchronously dq ?
pfnWdfIoTargetFormatRequestForRead dq ?
pfnWdfIoTargetSendWriteSynchronously dq	?
pfnWdfIoTargetFormatRequestForWrite dq ?
pfnWdfIoTargetSendIoctlSynchronously dq	?
pfnWdfIoTargetFormatRequestForIoctl dq ?
pfnWdfIoTargetSendInternalIoctlSynchronously dq	?
pfnWdfIoTargetFormatRequestForInternalIoctl dq ?
pfnWdfIoTargetSendInternalIoctlOthersSynchronously dq ?
pfnWdfIoTargetFormatRequestForInternalIoctlOthers dq ?
pfnWdfMemoryCreate dq ?
pfnWdfMemoryCreatePreallocated dq ?
pfnWdfMemoryGetBuffer dq ?
pfnWdfMemoryAssignBuffer dq ?
pfnWdfMemoryCopyToBuffer dq ?
pfnWdfMemoryCopyFromBuffer dq ?
pfnWdfLookasideListCreate dq ?
pfnWdfMemoryCreateFromLookaside	dq ?
pfnWdfDeviceMiniportCreate dq ?
pfnWdfDriverMiniportUnload dq ?
pfnWdfObjectGetTypedContextWorker dq ?
pfnWdfObjectAllocateContext dq ?
pfnWdfObjectContextGetObject dq	?
pfnWdfObjectReferenceActual dq ?
pfnWdfObjectDereferenceActual dq ?
pfnWdfObjectCreate dq ?
pfnWdfObjectDelete dq ?
pfnWdfObjectQuery dq ?
pfnWdfPdoInitAllocate dq ?
pfnWdfPdoInitSetEventCallbacks dq ?
pfnWdfPdoInitAssignDeviceID dq ?
pfnWdfPdoInitAssignInstanceID dq ?
pfnWdfPdoInitAddHardwareID dq ?
pfnWdfPdoInitAddCompatibleID dq	?
pfnWdfPdoInitAddDeviceText dq ?
pfnWdfPdoInitSetDefaultLocale dq ?
pfnWdfPdoInitAssignRawDevice dq	?
pfnWdfPdoMarkMissing dq	?
pfnWdfPdoRequestEject dq ?
pfnWdfPdoGetParent dq ?
pfnWdfPdoRetrieveIdentificationDescription dq ?
pfnWdfPdoRetrieveAddressDescription dq ?
pfnWdfPdoUpdateAddressDescription dq ?
pfnWdfPdoAddEjectionRelationsPhysicalDevice dq ?
pfnWdfPdoRemoveEjectionRelationsPhysicalDevice dq ?
pfnWdfPdoClearEjectionRelationsDevices dq ?
pfnWdfDeviceAddQueryInterface dq ?
pfnWdfRegistryOpenKey dq ?
pfnWdfRegistryCreateKey	dq ?
pfnWdfRegistryClose dq ?
pfnWdfRegistryWdmGetHandle dq ?
pfnWdfRegistryRemoveKey	dq ?
pfnWdfRegistryRemoveValue dq ?
pfnWdfRegistryQueryValue dq ?
pfnWdfRegistryQueryMemory dq ?
pfnWdfRegistryQueryMultiString dq ?
pfnWdfRegistryQueryUnicodeString dq ?
pfnWdfRegistryQueryString dq ?
pfnWdfRegistryQueryULong dq ?
pfnWdfRegistryAssignValue dq ?
pfnWdfRegistryAssignMemory dq ?
pfnWdfRegistryAssignMultiString	dq ?
pfnWdfRegistryAssignUnicodeString dq ?
pfnWdfRegistryAssignString dq ?
pfnWdfRegistryAssignULong dq ?
pfnWdfRequestCreate dq ?
pfnWdfRequestCreateFromIrp dq ?
pfnWdfRequestReuse dq ?
pfnWdfRequestChangeTarget dq ?
pfnWdfRequestFormatRequestUsingCurrentType dq ?
pfnWdfRequestWdmFormatUsingStackLocation dq ?
pfnWdfRequestSend dq ?
pfnWdfRequestGetStatus dq ?
pfnWdfRequestMarkCancelable dq ?
pfnWdfRequestUnmarkCancelable dq ?
pfnWdfRequestIsCanceled	dq ?
pfnWdfRequestCancelSentRequest dq ?
pfnWdfRequestIsFrom32BitProcess	dq ?
pfnWdfRequestSetCompletionRoutine dq ?
pfnWdfRequestGetCompletionParams dq ?
pfnWdfRequestAllocateTimer dq ?
pfnWdfRequestComplete dq ?
pfnWdfRequestCompleteWithPriorityBoost dq ?
pfnWdfRequestCompleteWithInformation dq	?
pfnWdfRequestGetParameters dq ?
pfnWdfRequestRetrieveInputMemory dq ?
pfnWdfRequestRetrieveOutputMemory dq ?
pfnWdfRequestRetrieveInputBuffer dq ?
pfnWdfRequestRetrieveOutputBuffer dq ?
pfnWdfRequestRetrieveInputWdmMdl dq ?
pfnWdfRequestRetrieveOutputWdmMdl dq ?
pfnWdfRequestRetrieveUnsafeUserInputBuffer dq ?
pfnWdfRequestRetrieveUnsafeUserOutputBuffer dq ?
pfnWdfRequestSetInformation dq ?
pfnWdfRequestGetInformation dq ?
pfnWdfRequestGetFileObject dq ?
pfnWdfRequestProbeAndLockUserBufferForRead dq ?
pfnWdfRequestProbeAndLockUserBufferForWrite dq ?
pfnWdfRequestGetRequestorMode dq ?
pfnWdfRequestForwardToIoQueue dq ?
pfnWdfRequestGetIoQueue	dq ?
pfnWdfRequestRequeue dq	?
pfnWdfRequestStopAcknowledge dq	?
pfnWdfRequestWdmGetIrp dq ?
pfnWdfIoResourceRequirementsListSetSlotNumber dq ?
pfnWdfIoResourceRequirementsListSetInterfaceType dq ?
pfnWdfIoResourceRequirementsListAppendIoResList	dq ?
pfnWdfIoResourceRequirementsListInsertIoResList	dq ?
pfnWdfIoResourceRequirementsListGetCount dq ?
pfnWdfIoResourceRequirementsListGetIoResList dq	?
pfnWdfIoResourceRequirementsListRemove dq ?
pfnWdfIoResourceRequirementsListRemoveByIoResList dq ?
pfnWdfIoResourceListCreate dq ?
pfnWdfIoResourceListAppendDescriptor dq	?
pfnWdfIoResourceListInsertDescriptor dq	?
pfnWdfIoResourceListUpdateDescriptor dq	?
pfnWdfIoResourceListGetCount dq	?
pfnWdfIoResourceListGetDescriptor dq ?
pfnWdfIoResourceListRemove dq ?
pfnWdfIoResourceListRemoveByDescriptor dq ?
pfnWdfCmResourceListAppendDescriptor dq	?
pfnWdfCmResourceListInsertDescriptor dq	?
pfnWdfCmResourceListGetCount dq	?
pfnWdfCmResourceListGetDescriptor dq ?
pfnWdfCmResourceListRemove dq ?
pfnWdfCmResourceListRemoveByDescriptor dq ?
pfnWdfStringCreate dq ?
pfnWdfStringGetUnicodeString dq	?
pfnWdfObjectAcquireLock	dq ?
pfnWdfObjectReleaseLock	dq ?
pfnWdfWaitLockCreate dq	?
pfnWdfWaitLockAcquire dq ?
pfnWdfWaitLockRelease dq ?
pfnWdfSpinLockCreate dq	?
pfnWdfSpinLockAcquire dq ?
pfnWdfSpinLockRelease dq ?
pfnWdfTimerCreate dq ?
pfnWdfTimerStart dq ?
pfnWdfTimerStop	dq ?
pfnWdfTimerGetParentObject dq ?
pfnWdfUsbTargetDeviceCreate dq ?
pfnWdfUsbTargetDeviceRetrieveInformation dq ?
pfnWdfUsbTargetDeviceGetDeviceDescriptor dq ?
pfnWdfUsbTargetDeviceRetrieveConfigDescriptor dq ?
pfnWdfUsbTargetDeviceQueryString dq ?
pfnWdfUsbTargetDeviceAllocAndQueryString dq ?
pfnWdfUsbTargetDeviceFormatRequestForString dq ?
pfnWdfUsbTargetDeviceGetNumInterfaces dq ?
pfnWdfUsbTargetDeviceSelectConfig dq ?
pfnWdfUsbTargetDeviceWdmGetConfigurationHandle dq ?
pfnWdfUsbTargetDeviceRetrieveCurrentFrameNumber	dq ?
pfnWdfUsbTargetDeviceSendControlTransferSynchronously dq ?
pfnWdfUsbTargetDeviceFormatRequestForControlTransfer dq	?
pfnWdfUsbTargetDeviceIsConnectedSynchronous dq ?
pfnWdfUsbTargetDeviceResetPortSynchronously dq ?
pfnWdfUsbTargetDeviceCyclePortSynchronously dq ?
pfnWdfUsbTargetDeviceFormatRequestForCyclePort dq ?
pfnWdfUsbTargetDeviceSendUrbSynchronously dq ?
pfnWdfUsbTargetDeviceFormatRequestForUrb dq ?
pfnWdfUsbTargetPipeGetInformation dq ?
pfnWdfUsbTargetPipeIsInEndpoint	dq ?
pfnWdfUsbTargetPipeIsOutEndpoint dq ?
pfnWdfUsbTargetPipeGetType dq ?
pfnWdfUsbTargetPipeSetNoMaximumPacketSizeCheck dq ?
pfnWdfUsbTargetPipeWriteSynchronously dq ?
pfnWdfUsbTargetPipeFormatRequestForWrite dq ?
pfnWdfUsbTargetPipeReadSynchronously dq	?
pfnWdfUsbTargetPipeFormatRequestForRead	dq ?
pfnWdfUsbTargetPipeConfigContinuousReader dq ?
pfnWdfUsbTargetPipeAbortSynchronously dq ?
pfnWdfUsbTargetPipeFormatRequestForAbort dq ?
pfnWdfUsbTargetPipeResetSynchronously dq ?
pfnWdfUsbTargetPipeFormatRequestForReset dq ?
pfnWdfUsbTargetPipeSendUrbSynchronously	dq ?
pfnWdfUsbTargetPipeFormatRequestForUrb dq ?
pfnWdfUsbInterfaceGetInterfaceNumber dq	?
pfnWdfUsbInterfaceGetNumEndpoints dq ?
pfnWdfUsbInterfaceGetDescriptor	dq ?
pfnWdfUsbInterfaceSelectSetting	dq ?
pfnWdfUsbInterfaceGetEndpointInformation dq ?
pfnWdfUsbTargetDeviceGetInterface dq ?
pfnWdfUsbInterfaceGetConfiguredSettingIndex dq ?
pfnWdfUsbInterfaceGetNumConfiguredPipes	dq ?
pfnWdfUsbInterfaceGetConfiguredPipe dq ?
pfnWdfUsbTargetPipeWdmGetPipeHandle dq ?
pfnWdfVerifierDbgBreakPoint dq ?
pfnWdfVerifierKeBugCheck dq ?
pfnWdfWmiProviderCreate	dq ?
pfnWdfWmiProviderGetDevice dq ?
pfnWdfWmiProviderIsEnabled dq ?
pfnWdfWmiProviderGetTracingHandle dq ?
pfnWdfWmiInstanceCreate	dq ?
pfnWdfWmiInstanceRegister dq ?
pfnWdfWmiInstanceDeregister dq ?
pfnWdfWmiInstanceGetDevice dq ?
pfnWdfWmiInstanceGetProvider dq	?
pfnWdfWmiInstanceFireEvent dq ?
pfnWdfWorkItemCreate dq	?
pfnWdfWorkItemEnqueue dq ?
pfnWdfWorkItemGetParentObject dq ?
pfnWdfWorkItemFlush dq ?
pfnWdfCommonBufferCreateWithConfig dq ?
pfnWdfDmaEnablerGetFragmentLength dq ?
pfnWdfDmaEnablerWdmGetDmaAdapter dq ?
pfnWdfUsbInterfaceGetNumSettings dq ?
pfnWdfDeviceRemoveDependentUsageDeviceObject dq	?
pfnWdfDeviceGetSystemPowerAction dq ?
pfnWdfInterruptSetExtendedPolicy dq ?
pfnWdfIoQueueAssignForwardProgressPolicy dq ?
pfnWdfPdoInitAssignContainerID dq ?
pfnWdfPdoInitAllowForwardingRequestToParent dq ?
pfnWdfRequestMarkCancelableEx dq ?
pfnWdfRequestIsReserved	dq ?
pfnWdfRequestForwardToParentDeviceIoQueue dq ?
pfnWdfCxDeviceInitAllocate dq ?
pfnWdfCxDeviceInitAssignWdmIrpPreprocessCallback dq ?
pfnWdfCxDeviceInitSetIoInCallerContextCallback dq ?
pfnWdfCxDeviceInitSetRequestAttributes dq ?
pfnWdfCxDeviceInitSetFileObjectConfig dq ?
pfnWdfDeviceWdmDispatchIrp dq ?
pfnWdfDeviceWdmDispatchIrpToIoQueue dq ?
pfnWdfDeviceInitSetRemoveLockOptions dq	?
pfnWdfDeviceConfigureWdmIrpDispatchCallback dq ?
pfnWdfDmaEnablerConfigureSystemProfile dq ?
pfnWdfDmaTransactionInitializeUsingOffset dq ?
pfnWdfDmaTransactionGetTransferInfo dq ?
pfnWdfDmaTransactionSetChannelConfigurationCallback dq ?
pfnWdfDmaTransactionSetTransferCompleteCallback	dq ?
pfnWdfDmaTransactionSetImmediateExecution dq ?
pfnWdfDmaTransactionAllocateResources dq ?
pfnWdfDmaTransactionSetDeviceAddressOffset dq ?
pfnWdfDmaTransactionFreeResources dq ?
pfnWdfDmaTransactionCancel dq ?
pfnWdfDmaTransactionWdmGetTransferContext dq ?
pfnWdfInterruptQueueWorkItemForIsr dq ?
pfnWdfInterruptTryToAcquireLock	dq ?
pfnWdfIoQueueStopAndPurge dq ?
pfnWdfIoQueueStopAndPurgeSynchronously dq ?
pfnWdfIoTargetPurge dq ?
pfnWdfUsbTargetDeviceCreateWithParameters dq ?
pfnWdfUsbTargetDeviceQueryUsbCapability	dq ?
pfnWdfUsbTargetDeviceCreateUrb dq ?
pfnWdfUsbTargetDeviceCreateIsochUrb dq ?
pfnWdfDeviceWdmAssignPowerFrameworkSettings dq ?
pfnWdfDmaTransactionStopSystemTransfer dq ?
pfnWdfCxVerifierKeBugCheck dq ?
pfnWdfInterruptReportActive dq ?
pfnWdfInterruptReportInactive dq ?
pfnWdfDeviceInitSetReleaseHardwareOrderOnFailure dq ?
pfnWdfGetTriageInfo dq ?
WDFFUNCTIONS	ends

; ---------------------------------------------------------------------------

; enum MM_PAGE_PRIORITY, copyof_13
LowPagePriority	 = 0
NormalPagePriority  = 10h
HighPagePriority  = 20h

;
; +-------------------------------------------------------------------------+
; |   This file	has been generated by The Interactive Disassembler (IDA)    |
; |	      Copyright	(c) 2015 Hex-Rays, <support@hex-rays.com>	    |
; |			 License info: 48-B611-7234-BB			    |
; |		Doskey Lee, Kingsoft Internet Security Software		    |
; +-------------------------------------------------------------------------+
;
; Input	MD5   :	6FE4DEC144AFE13AD58F9B4FE8E9331D
; Input	CRC32 :	3A468AB5

; File Name   :	C:\Users\benoit\work\fhv.sys
; Format      :	Portable executable for	AMD64 (PE)
; Imagebase   :	140000000
; Section 1. (virtual address 00001000)
; Virtual size			: 000040FD (  16637.)
; Section size in file		: 00004200 (  16896.)
; Offset to raw	data for section: 00000400
; Flags	68000020: Text Not pageable Executable Readable
; Alignment	: default
; PDB File Name	: ASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASD\toobadsoosadd.pdb

		include	uni.inc	; see unicode subdir of	ida for	info on	unicode

		.686p
		.mmx
		.model flat

; ===========================================================================

; Segment type:	Pure code
; Segment permissions: Read/Execute
_text		segment	para public 'CODE' use64
		assume cs:_text
		;org 140001000h
		assume es:nothing, ss:nothing, ds:_data, fs:nothing, gs:nothing

; =============== S U B	R O U T	I N E =======================================


unbind_stuff	proc near		; CODE XREF: j_unbind_stuffj
					; driver_unload_func+22j ...
		sub	rsp, 28h
		lea	rcx, wdf_version
		call	sub_1400011B0
		mov	r8, qword ptr cs:wdf_globals
		lea	rdx, wdf_version
		lea	rcx, unk_140009928
		add	rsp, 28h
		jmp	WdfVersionUnbind
unbind_stuff	endp

; ---------------------------------------------------------------------------
algn_14000102E:				; DATA XREF: .pdata:ExceptionDiro
		align 10h
; [00000005 BYTES: COLLAPSED FUNCTION j_unbind_stuff. PRESS CTRL-NUMPAD+ TO EXPAND]
		align 8

; =============== S U B	R O U T	I N E =======================================


driver_unload_func proc	near		; DATA XREF: driver_unload_func+10o
					; drivermain+D3o ...
		sub	rsp, 28h
		mov	rax, qword ptr cs:unk_140009938
		test	rax, rax
		jz	short loc_140001056
		lea	rdx, driver_unload_func
		cmp	rax, rdx
		jz	short loc_140001056
		call	rax ; unk_140009938

loc_140001056:				; CODE XREF: driver_unload_func+Ej
					; driver_unload_func+1Aj
		add	rsp, 28h
		jmp	unbind_stuff
driver_unload_func endp

; ---------------------------------------------------------------------------
algn_14000105F:				; DATA XREF: .pdata:000000014000A00Co
		align 20h

; =============== S U B	R O U T	I N E =======================================


drivermain	proc near		; CODE XREF: DriverEntry+25j
					; DATA XREF: .pdata:000000014000A018o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		mov	[rsp+arg_10], rsi
		push	rdi
		sub	rsp, 20h
		xor	ebp, ebp
		mov	rsi, rdx
		mov	rdi, rcx
		cmp	rcx, rbp
		jnz	short loc_14000108D
		xor	ecx, ecx
		call	main_run_stuff
		jmp	loc_14000116D
; ---------------------------------------------------------------------------

loc_14000108D:				; CODE XREF: drivermain+1Fj
		mov	eax, 208h
		mov	qword ptr cs:unk_140009950, rcx
		lea	rcx, unk_140009928 ; DestinationString
		mov	word ptr cs:unk_14000992A, ax
		lea	rax, unk_140009960
		mov	word ptr cs:unk_140009928, bp
		mov	qword ptr cs:unk_140009930, rax
		call	cs:RtlCopyUnicodeString
		lea	r9, wdf_globals
		lea	r8, wdf_version
		lea	rdx, unk_140009928
		mov	rcx, rdi
		call	WdfVersionBind
		cmp	eax, ebp
		jl	loc_14000116D
		lea	rcx, wdf_version
		call	maybe_useless
		cmp	eax, ebp
		mov	ebx, eax
		jl	short loc_140001166
		call	maybe_useless_v2
		mov	rdx, rsi
		mov	rcx, rdi
		call	main_run_stuff
		cmp	eax, ebp
		mov	ebx, eax
		jl	short loc_140001166
		mov	rax, qword ptr cs:wdf_globals
		cmp	[rax+30h], bpl
		jz	short loc_140001140
		mov	rax, qword ptr cs:unk_140009938
		cmp	[rdi+68h], rbp
		cmovnz	rax, [rdi+68h]
		mov	qword ptr cs:unk_140009938, rax
		lea	rax, driver_unload_func
		mov	[rdi+68h], rax
		jmp	short loc_140001162
; ---------------------------------------------------------------------------

loc_140001140:				; CODE XREF: drivermain+BAj
		test	byte ptr [rax+8], 2
		jz	short loc_140001162
		mov	rax, qword ptr cs:unk_140009308
		mov	qword ptr cs:unk_140009940, rax
		lea	rax, j_unbind_stuff
		mov	qword ptr cs:unk_140009308, rax

loc_140001162:				; CODE XREF: drivermain+DEj
					; drivermain+E4j
		xor	eax, eax
		jmp	short loc_14000116D
; ---------------------------------------------------------------------------

loc_140001166:				; CODE XREF: drivermain+97j
					; drivermain+ADj
		call	unbind_stuff
		mov	eax, ebx

loc_14000116D:				; CODE XREF: drivermain+28j
					; drivermain+81j ...
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		add	rsp, 20h
		pop	rdi
		retn
drivermain	endp

; ---------------------------------------------------------------------------
algn_140001182:				; DATA XREF: .pdata:000000014000A018o
		align 4

; =============== S U B	R O U T	I N E =======================================


; NTSTATUS __stdcall DriverEntry(PDRIVER_OBJECT	DriverObject, PUNICODE_STRING RegistryPath)
		public DriverEntry
DriverEntry	proc near		; DATA XREF: .pdata:000000014000A024o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, rdx
		mov	rdi, rcx
		call	cookie_func1
		mov	rdx, rbx
		mov	rcx, rdi
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	drivermain
DriverEntry	endp

; ---------------------------------------------------------------------------
algn_1400011AE:				; DATA XREF: .pdata:000000014000A024o
		align 10h

; =============== S U B	R O U T	I N E =======================================


sub_1400011B0	proc near		; CODE XREF: unbind_stuff+Bp
					; DATA XREF: .pdata:000000014000A030o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rax, cs:off_140007078
		mov	rdi, rcx
		lea	rcx, unk_140007060
		lea	rbx, unk_140007070
		cmp	rax, rcx
		jz	short loc_14000121C
		cmp	rbx, rax
		ja	short loc_14000121C

loc_1400011DC:				; CODE XREF: sub_1400011B0+6Aj
		mov	rax, [rbx+40h]
		test	rax, rax
		jz	short loc_1400011FD
		mov	r8, qword ptr cs:wdf_globals
		lea	rcx, WdfVersionUnbindClass
		mov	r9, rbx
		mov	rdx, rdi
		call	rax
		jmp	short loc_14000120F
; ---------------------------------------------------------------------------

loc_1400011FD:				; CODE XREF: sub_1400011B0+33j
		mov	rdx, qword ptr cs:wdf_globals
		mov	r8, rbx
		mov	rcx, rdi
		call	WdfVersionUnbindClass

loc_14000120F:				; CODE XREF: sub_1400011B0+4Bj
		add	rbx, 50h
		cmp	rbx, cs:off_140007078
		jbe	short loc_1400011DC

loc_14000121C:				; CODE XREF: sub_1400011B0+25j
					; sub_1400011B0+2Aj
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
sub_1400011B0	endp

; ---------------------------------------------------------------------------
algn_140001227:				; DATA XREF: .pdata:000000014000A030o
		align 8

; =============== S U B	R O U T	I N E =======================================


maybe_useless	proc near		; CODE XREF: drivermain+8Ep
					; DATA XREF: .pdata:000000014000A03Co

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, rcx
		xor	eax, eax
		lea	rbx, unk_140007070
		lea	rsi, unk_140007070

loc_14000124A:				; CODE XREF: maybe_useless+6Ej
		cmp	rbx, rsi
		jnb	short loc_14000129D
		cmp	dword ptr [rbx], 50h
		jnz	short loc_140001298
		mov	rax, [rbx+38h]
		mov	cs:off_140007078, rbx
		test	rax, rax
		jz	short loc_14000127C
		mov	r8, qword ptr cs:wdf_globals
		lea	rcx, WdfVersionBindClass
		mov	r9, rbx
		mov	rdx, rdi
		call	rax
		jmp	short loc_14000128E
; ---------------------------------------------------------------------------

loc_14000127C:				; CODE XREF: maybe_useless+3Aj
		mov	rdx, qword ptr cs:wdf_globals
		mov	r8, rbx
		mov	rcx, rdi
		call	WdfVersionBindClass

loc_14000128E:				; CODE XREF: maybe_useless+52j
		test	eax, eax
		js	short loc_14000129D
		add	rbx, 50h
		jmp	short loc_14000124A
; ---------------------------------------------------------------------------

loc_140001298:				; CODE XREF: maybe_useless+2Aj
		mov	eax, 0C0000004h

loc_14000129D:				; CODE XREF: maybe_useless+25j
					; maybe_useless+68j
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		retn
maybe_useless	endp

; ---------------------------------------------------------------------------
algn_1400012AD:				; DATA XREF: .pdata:000000014000A03Co
		align 10h

; =============== S U B	R O U T	I N E =======================================


maybe_useless_v2 proc near		; CODE XREF: drivermain+99p
					; DATA XREF: .pdata:000000014000A048o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		lea	rax, unk_140007090
		lea	rcx, unk_140007090
		cmp	rax, rcx
		jnb	short loc_140001309
		sub	rcx, rax
		mov	rax, 0CCCCCCCCCCCCCCCDh
		lea	rbx, unk_1400070B0
		dec	rcx
		mul	rcx
		mov	rdi, rdx
		shr	rdi, 5
		inc	rdi

loc_1400012F1:				; CODE XREF: maybe_useless_v2+57j
		mov	rax, [rbx]
		test	rax, rax
		jz	short loc_1400012FF
		call	rax
		mov	[rbx-8], rax

loc_1400012FF:				; CODE XREF: maybe_useless_v2+47j
		add	rbx, 28h
		sub	rdi, 1
		jnz	short loc_1400012F1

loc_140001309:				; CODE XREF: maybe_useless_v2+1Bj
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
maybe_useless_v2 endp

; ---------------------------------------------------------------------------
algn_140001314:				; DATA XREF: .pdata:000000014000A048o
		align 20h

; =============== S U B	R O U T	I N E =======================================


run_cb1		proc near		; CODE XREF: gogolaunch_wrap+Ep
		pushfq
		push	rax
		push	rcx
		push	rdx
		push	rbx
		push	0FFFFFFFFFFFFFFFFh
		push	rbp
		push	rsi
		push	rdi
		push	r8
		push	r9
		push	r10
		push	r11
		push	r12
		push	r13
		push	r14
		push	r15
		mov	rax, rcx
		mov	r8, rdx
		mov	rdx, offset guest_rip
		mov	rcx, rsp
		sub	rsp, 20h
		call	rax
		add	rsp, 20h
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	r11
		pop	r10
		pop	r9
		pop	r8
		pop	rdi
		pop	rsi
		pop	rbp
		add	rsp, 8
		pop	rbx
		pop	rdx
		pop	rcx
		pop	rax
		popfq
		xor	rax, rax
		retn
run_cb1		endp

; ---------------------------------------------------------------------------
guest_rip	db 90h			; DATA XREF: run_cb1+20o
; ---------------------------------------------------------------------------
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	r11
		pop	r10
		pop	r9
		pop	r8
		pop	rdi
		pop	rsi
		pop	rbp
		add	rsp, 8
		pop	rbx
		pop	rdx
		pop	rcx
		pop	rax
		popfq
		sub	rsp, 8
		pushfq
		push	rax
		push	rcx
		push	rdx
		push	rbx
		push	0FFFFFFFFFFFFFFFFh
		push	rbp
		push	rsi
		push	rdi
		push	r8
		push	r9
		push	r10
		push	r11
		push	r12
		push	r13
		push	r14
		push	r15
		mov	rcx, rsp
		mov	rdx, rsp
		add	rdx, 88h
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	r11
		pop	r10
		pop	r9
		pop	r8
		pop	rdi
		pop	rsi
		pop	rbp
		add	rsp, 8
		pop	rbx
		pop	rdx
		pop	rcx
		pop	rax
		popfq
		add	rsp, 8
		xor	rax, rax
		inc	rax
		retn

; =============== S U B	R O U T	I N E =======================================


ENTRY_FUNC	proc near		; DATA XREF: sub_14000BE30+7B3o

var_E0		= xmmword ptr -0E0h
var_D0		= xmmword ptr -0D0h
var_C0		= xmmword ptr -0C0h
var_B0		= xmmword ptr -0B0h
var_A0		= xmmword ptr -0A0h
var_90		= xmmword ptr -90h

		push	rax
		push	rcx
		push	rdx
		push	rbx
		push	0FFFFFFFFFFFFFFFFh
		push	rbp
		push	rsi
		push	rdi
		push	r8
		push	r9
		push	r10
		push	r11
		push	r12
		push	r13
		push	r14
		push	r15
		mov	rcx, rsp
		sub	rsp, 60h
		movaps	[rsp+0E0h+var_E0], xmm0
		movaps	[rsp+0E0h+var_D0], xmm1
		movaps	[rsp+0E0h+var_C0], xmm2
		movaps	[rsp+0E0h+var_B0], xmm3
		movaps	[rsp+0E0h+var_A0], xmm4
		movaps	[rsp+0E0h+var_90], xmm5
		sub	rsp, 20h
		call	VM_ENTRY_HANDLER
		add	rsp, 20h
		movaps	xmm0, [rsp+0E0h+var_E0]
		movaps	xmm1, [rsp+0E0h+var_D0]
		movaps	xmm2, [rsp+0E0h+var_C0]
		movaps	xmm3, [rsp+0E0h+var_B0]
		movaps	xmm4, [rsp+0E0h+var_A0]
		movaps	xmm5, [rsp+0E0h+var_90]
		add	rsp, 60h
		test	al, al
		jz	short loc_140001475
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	r11
		pop	r10
		pop	r9
		pop	r8
		pop	rdi
		pop	rsi
		pop	rbp
		add	rsp, 8
		pop	rbx
		pop	rdx
		pop	rcx
		pop	rax
		vmresume
		jmp	short loc_14000149E
; ---------------------------------------------------------------------------

loc_140001475:				; CODE XREF: ENTRY_FUNC+6Dj
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	r11
		pop	r10
		pop	r9
		pop	r8
		pop	rdi
		pop	rsi
		pop	rbp
		add	rsp, 8
		pop	rbx
		pop	rdx
		pop	rcx
		pop	rax
		vmxoff
		jz	short loc_14000149E
		jb	short loc_14000149E
		push	rax
		popfq
		mov	rsp, rdx
		push	rcx
		retn
; ---------------------------------------------------------------------------

loc_14000149E:				; CODE XREF: ENTRY_FUNC+8Dj
					; ENTRY_FUNC+ADj ...
		pushfq
		push	rax
		push	rcx
		push	rdx
		push	rbx
		push	0FFFFFFFFFFFFFFFFh
		push	rbp
		push	rsi
		push	rdi
		push	r8
		push	r9
		push	r10
		push	r11
		push	r12
		push	r13
		push	r14
		push	r15
		mov	rcx, rsp
		sub	rsp, 28h
		call	sub_1400030B8
		add	rsp, 28h
		int	3		; Trap to Debugger
ENTRY_FUNC	endp ; sp-analysis failed


; =============== S U B	R O U T	I N E =======================================


do_vmcall	proc near		; CODE XREF: vm_call_wrapper+6p
		vmcall
		jz	short loc_1400014DC
		jb	short loc_1400014D4
		xor	rax, rax
		retn
; ---------------------------------------------------------------------------

loc_1400014D4:				; CODE XREF: do_vmcall+5j
		mov	rax, 2
		retn
; ---------------------------------------------------------------------------

loc_1400014DC:				; CODE XREF: do_vmcall+3j
		mov	rax, 1
		retn
do_vmcall	endp


; =============== S U B	R O U T	I N E =======================================


sub_1400014E4	proc near		; CODE XREF: sub_140004440+72p
		lgdt	fword ptr [rcx]
		retn
sub_1400014E4	endp


; =============== S U B	R O U T	I N E =======================================


sub_1400014E8	proc near		; CODE XREF: sub_14000BE30+45p
		sgdt	fword ptr [rcx]
		retn
sub_1400014E8	endp

; ---------------------------------------------------------------------------
		dd 0C3D1000Fh

; =============== S U B	R O U T	I N E =======================================


sub_1400014F0	proc near		; CODE XREF: sub_14000BA30+1Ep
					; sub_14000BE30+1E8p ...
		sldt	ax
		retn
sub_1400014F0	endp

; ---------------------------------------------------------------------------
		db 0Fh,	0, 0D9h
; ---------------------------------------------------------------------------
		retn

; =============== S U B	R O U T	I N E =======================================


sub_1400014F9	proc near		; CODE XREF: sub_14000BE30+1FAp
					; sub_14000BE30+29Cp ...
		str	ax
		retn
sub_1400014F9	endp

; ---------------------------------------------------------------------------
		db  66h	; f
		db  8Eh	; é
; ---------------------------------------------------------------------------

loc_140001500:				; CODE XREF: sub_14000BE30+17Cp
					; sub_14000BE30+20Cp ...
		rol	ebx, 66h
		mov	eax, es
		retn
; ---------------------------------------------------------------------------
		dw 8E66h
; ---------------------------------------------------------------------------
		leave
		retn

; =============== S U B	R O U T	I N E =======================================


sub_14000150A	proc near		; CODE XREF: sub_14000BE30+18Ep
					; sub_14000BE30+224p ...
		mov	ax, cs
		retn
sub_14000150A	endp

; ---------------------------------------------------------------------------
		mov	ss, cx
		retn

; =============== S U B	R O U T	I N E =======================================


sub_140001512	proc near		; CODE XREF: sub_14000BE30+1A0p
					; sub_14000BE30+23Cp ...
		mov	ax, ss
		retn
sub_140001512	endp

; ---------------------------------------------------------------------------
		mov	ds, cx
		retn

; =============== S U B	R O U T	I N E =======================================


sub_14000151A	proc near		; CODE XREF: sub_14000BE30+1B2p
					; sub_14000BE30+254p ...
		mov	ax, ds
		retn
sub_14000151A	endp

; ---------------------------------------------------------------------------
		mov	fs, cx
		retn

; =============== S U B	R O U T	I N E =======================================


sub_140001522	proc near		; CODE XREF: sub_14000BE30+1C4p
					; sub_14000BE30+26Cp ...
		mov	ax, fs
		retn
sub_140001522	endp

; ---------------------------------------------------------------------------
		dw 8E66h
byte_140001528	db 0E9h, 0C3h, 66h, 8Ch, 0E8h, 0C3h ; CODE XREF: sub_14000BE30+1D6p
					; sub_14000BE30+284p ...
word_14000152E	dw 0F48h		; CODE XREF: sub_14000BA08+Ep
; ---------------------------------------------------------------------------
		add	al, cl
		retn

; =============== S U B	R O U T	I N E =======================================


sub_140001533	proc near		; CODE XREF: real_handler:loc_1400045AEp
		invd
		retn
sub_140001533	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001536	proc near		; CODE XREF: handle_exit_intr+62p
		mov	cr2, rcx
		retn
sub_140001536	endp


; =============== S U B	R O U T	I N E =======================================


sub_14000153A	proc near		; CODE XREF: sub_140002D30+27p
		invept	ecx, xmmword ptr [rdx]
		jz	short loc_14000154F
		jb	short loc_140001547
		xor	rax, rax
		retn
; ---------------------------------------------------------------------------

loc_140001547:				; CODE XREF: sub_14000153A+7j
		mov	rax, 2
		retn
; ---------------------------------------------------------------------------

loc_14000154F:				; CODE XREF: sub_14000153A+5j
		mov	rax, 1
		retn
sub_14000153A	endp


; =============== S U B	R O U T	I N E =======================================


some_invpid	proc near		; CODE XREF: sub_140002D70+27p
					; invpid_wrap+2Bp ...
		invvpid	ecx, xmmword ptr [rdx]
		jz	short loc_14000156C
		jb	short loc_140001564
		xor	rax, rax
		retn
; ---------------------------------------------------------------------------

loc_140001564:				; CODE XREF: some_invpid+7j
		mov	rax, 2
		retn
; ---------------------------------------------------------------------------

loc_14000156C:				; CODE XREF: some_invpid+5j
		mov	rax, 1
		retn
some_invpid	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001574	proc near		; CODE XREF: sub_140001780+1Cp
					; sub_1400017C8+1Fp ...
		cmp	ecx, edx
		pushfq
		pop	rax
		retn
sub_140001574	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001579	proc near		; CODE XREF: sub_140001CB8+86p
		movsx	eax, byte ptr [rdx]
		mov	[rcx], rax
		retn
sub_140001579	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001580	proc near		; CODE XREF: sub_140001D74+5Ep
		movsxd	rax, dword ptr [rdx]
		mov	[rcx], rax
		retn
sub_140001580	endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140001588	proc near		; CODE XREF: sub_14000B000+44p
		mov	rax, cs:KdDebuggerNotPresent
		cmp	byte ptr [rax],	0
		jnz	short locret_140001595
		int	3		; Trap to Debugger

locret_140001595:			; CODE XREF: sub_140001588+Aj
		retn
sub_140001588	endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140001598	proc near		; CODE XREF: sub_140001744+15p
					; sub_1400017C8+15p ...
		mov	al, [rdx]
		add	al, 9
		cmp	al, 0F4h
		jnz	short loc_1400015A5
		lea	rax, [rcx+10h]
		retn
; ---------------------------------------------------------------------------

loc_1400015A5:				; CODE XREF: sub_140001598+6j
		cmp	al, 0EEh
		jnz	short loc_1400015B1
		mov	rax, [rcx]
		add	rax, 78h
		retn
; ---------------------------------------------------------------------------

loc_1400015B1:				; CODE XREF: sub_140001598+Fj
		cmp	al, 0EFh
		jnz	short loc_1400015BD
		mov	rax, [rcx]
		add	rax, 60h
		retn
; ---------------------------------------------------------------------------

loc_1400015BD:				; CODE XREF: sub_140001598+1Bj
		cmp	al, 0F0h
		jnz	short loc_1400015C9
		mov	rax, [rcx]
		add	rax, 70h
		retn
; ---------------------------------------------------------------------------

loc_1400015C9:				; CODE XREF: sub_140001598+27j
		cmp	al, 0F1h
		jnz	short loc_1400015D5
		mov	rax, [rcx]
		add	rax, 68h
		retn
; ---------------------------------------------------------------------------

loc_1400015D5:				; CODE XREF: sub_140001598+33j
		cmp	al, 0F2h
		jnz	short loc_1400015E1
		mov	rax, [rcx]
		add	rax, 48h
		retn
; ---------------------------------------------------------------------------

loc_1400015E1:				; CODE XREF: sub_140001598+3Fj
		cmp	al, 0F3h
		jnz	short loc_1400015ED
		mov	rax, [rcx]
		add	rax, 40h
		retn
; ---------------------------------------------------------------------------

loc_1400015ED:				; CODE XREF: sub_140001598+4Bj
		cmp	al, 0F5h
		jnz	short loc_1400015F9
		mov	rax, [rcx]
		add	rax, 58h
		retn
; ---------------------------------------------------------------------------

loc_1400015F9:				; CODE XREF: sub_140001598+57j
		cmp	al, 0F6h
		jnz	short loc_140001605
		mov	rax, [rcx]
		add	rax, 50h
		retn
; ---------------------------------------------------------------------------

loc_140001605:				; CODE XREF: sub_140001598+63j
		xor	eax, eax
		retn
sub_140001598	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001608	proc near		; CODE XREF: sub_1400016EC+1Ap
					; sub_1400016EC+29p ...
		mov	al, [rdx]
		cmp	al, 0F4h
		jnz	short loc_140001613
		lea	rax, [rcx+10h]
		retn
; ---------------------------------------------------------------------------

loc_140001613:				; CODE XREF: sub_140001608+4j
		cmp	al, 0EEh
		jnz	short loc_14000161F
		mov	rax, [rcx]
		add	rax, 78h
		retn
; ---------------------------------------------------------------------------

loc_14000161F:				; CODE XREF: sub_140001608+Dj
		cmp	al, 0EFh
		jnz	short loc_14000162B
		mov	rax, [rcx]
		add	rax, 60h
		retn
; ---------------------------------------------------------------------------

loc_14000162B:				; CODE XREF: sub_140001608+19j
		cmp	al, 0F0h
		jnz	short loc_140001637
		mov	rax, [rcx]
		add	rax, 70h
		retn
; ---------------------------------------------------------------------------

loc_140001637:				; CODE XREF: sub_140001608+25j
		cmp	al, 0F1h
		jnz	short loc_140001643
		mov	rax, [rcx]
		add	rax, 68h
		retn
; ---------------------------------------------------------------------------

loc_140001643:				; CODE XREF: sub_140001608+31j
		cmp	al, 0F2h
		jnz	short loc_14000164F
		mov	rax, [rcx]
		add	rax, 48h
		retn
; ---------------------------------------------------------------------------

loc_14000164F:				; CODE XREF: sub_140001608+3Dj
		cmp	al, 0F3h
		jnz	short loc_14000165B
		mov	rax, [rcx]
		add	rax, 40h
		retn
; ---------------------------------------------------------------------------

loc_14000165B:				; CODE XREF: sub_140001608+49j
		cmp	al, 0F5h
		jnz	short loc_140001667
		mov	rax, [rcx]
		add	rax, 58h
		retn
; ---------------------------------------------------------------------------

loc_140001667:				; CODE XREF: sub_140001608+55j
		cmp	al, 0F6h
		jnz	short loc_140001673
		mov	rax, [rcx]
		add	rax, 50h
		retn
; ---------------------------------------------------------------------------

loc_140001673:				; CODE XREF: sub_140001608+61j
		cmp	al, 0F7h
		jnz	short loc_14000167F
		mov	rax, [rcx]
		add	rax, 38h
		retn
; ---------------------------------------------------------------------------

loc_14000167F:				; CODE XREF: sub_140001608+6Dj
		cmp	al, 0F8h
		jnz	short loc_14000168B
		mov	rax, [rcx]
		add	rax, 30h
		retn
; ---------------------------------------------------------------------------

loc_14000168B:				; CODE XREF: sub_140001608+79j
		cmp	al, 0F9h
		jnz	short loc_140001697
		mov	rax, [rcx]
		add	rax, 28h
		retn
; ---------------------------------------------------------------------------

loc_140001697:				; CODE XREF: sub_140001608+85j
		cmp	al, 0FAh
		jnz	short loc_1400016A3
		mov	rax, [rcx]
		add	rax, 20h
		retn
; ---------------------------------------------------------------------------

loc_1400016A3:				; CODE XREF: sub_140001608+91j
		cmp	al, 0FBh
		jnz	short loc_1400016AF
		mov	rax, [rcx]
		add	rax, 18h
		retn
; ---------------------------------------------------------------------------

loc_1400016AF:				; CODE XREF: sub_140001608+9Dj
		cmp	al, 0FCh
		jnz	short loc_1400016BB
		mov	rax, [rcx]
		add	rax, 10h
		retn
; ---------------------------------------------------------------------------

loc_1400016BB:				; CODE XREF: sub_140001608+A9j
		cmp	al, 0FDh
		jnz	short loc_1400016C7
		mov	rax, [rcx]
		add	rax, 8
		retn
; ---------------------------------------------------------------------------

loc_1400016C7:				; CODE XREF: sub_140001608+B5j
		cmp	al, 0FEh
		jnz	short loc_1400016CF
		mov	rax, [rcx]
		retn
; ---------------------------------------------------------------------------

loc_1400016CF:				; CODE XREF: sub_140001608+C1j
		xor	eax, eax
		retn
sub_140001608	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400016D4	proc near		; CODE XREF: sub_1400023AC+1C6p
		mov	rax, [rcx+10h]
		mov	ecx, 681Eh
		movsx	rdx, word ptr [rax+1]
		add	rdx, rax
		jmp	do_vm_write
sub_1400016D4	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400016EC	proc near		; CODE XREF: sub_1400023AC+62p
					; DATA XREF: .pdata:000000014000A054o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+2]
		call	sub_140001608
		lea	rdx, [rdi+1]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001608
		mov	ecx, 681Eh
		mov	rdx, [rax]
		add	[rbx], rdx
		mov	rdx, [rsi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_1400016EC	endp

; ---------------------------------------------------------------------------
algn_140001741:				; DATA XREF: .pdata:000000014000A054o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001744	proc near		; CODE XREF: sub_1400023AC+2B7p
					; DATA XREF: .pdata:000000014000A060o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	edx, [rbx+2]
		mov	ecx, 681Eh
		and	[rax], edx
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001744	endp

; ---------------------------------------------------------------------------
algn_14000177F:				; DATA XREF: .pdata:000000014000A060o
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140001780	proc near		; CODE XREF: sub_1400023AC+1B2p
					; DATA XREF: .pdata:000000014000A06Co
		push	rbx
		sub	rsp, 20h
		mov	rdx, [rcx+10h]
		mov	rbx, rcx
		mov	rax, [rcx]
		mov	ecx, [rdx+1]
		add	rcx, [rax+58h]
		mov	edx, [rdx+5]
		mov	ecx, [rcx]
		call	sub_140001574
		mov	rdx, rax
		mov	ecx, 6820h
		call	do_vm_write
		mov	rdx, [rbx+10h]
		mov	ecx, 681Eh
		add	rdx, 9
		add	rsp, 20h
		pop	rbx
		jmp	do_vm_write
sub_140001780	endp

; ---------------------------------------------------------------------------
algn_1400017C5:				; DATA XREF: .pdata:000000014000A06Co
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_1400017C8	proc near		; CODE XREF: sub_1400023AC+2E4p
					; DATA XREF: .pdata:000000014000A078o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	edx, [rbx+2]
		mov	ecx, [rax]
		call	sub_140001574
		mov	rdx, rax
		mov	ecx, 6820h
		call	do_vm_write
		mov	rdx, [rdi+10h]
		mov	ecx, 681Eh
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_1400017C8	endp

; ---------------------------------------------------------------------------
algn_140001815:				; DATA XREF: .pdata:000000014000A078o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140001818	proc near		; CODE XREF: sub_1400023AC+1A1p
					; DATA XREF: .pdata:000000014000A084o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+1]
		call	sub_140001598
		lea	rdx, [rdi+2]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001598
		mov	ecx, [rbx]
		mov	edx, [rax]
		call	sub_140001574
		mov	rdx, rax
		mov	ecx, 6820h
		call	do_vm_write
		mov	rdx, [rsi+10h]
		mov	ecx, 681Eh
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001818	endp

; ---------------------------------------------------------------------------
algn_14000187D:				; DATA XREF: .pdata:000000014000A084o
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140001880	proc near		; CODE XREF: sub_1400023AC+1FCp
		mov	rdx, [rcx+8]
		mov	r8, [rcx+10h]
		test	dl, 40h
		jnz	short loc_14000189E
		mov	rax, rdx
		shr	rax, 4
		xor	al, dl
		jns	short loc_14000189E
		lea	rdx, [r8+3]
		jmp	short loc_1400018A6
; ---------------------------------------------------------------------------

loc_14000189E:				; CODE XREF: sub_140001880+Bj
					; sub_140001880+16j
		movsx	rdx, word ptr [r8+1]
		add	rdx, r8

loc_1400018A6:				; CODE XREF: sub_140001880+1Cj
		mov	ecx, 681Eh
		jmp	do_vm_write
sub_140001880	endp


; =============== S U B	R O U T	I N E =======================================


sub_1400018B0	proc near		; CODE XREF: sub_1400023AC+1D8p
		test	byte ptr [rcx+8], 40h
		jnz	short loc_1400018C4
		mov	rax, [rcx+10h]
		movsx	rdx, word ptr [rax+1]
		add	rdx, rax
		jmp	short loc_1400018CC
; ---------------------------------------------------------------------------

loc_1400018C4:				; CODE XREF: sub_1400018B0+4j
		mov	rdx, [rcx+10h]
		add	rdx, 3

loc_1400018CC:				; CODE XREF: sub_1400018B0+12j
		mov	ecx, 681Eh
		jmp	do_vm_write
sub_1400018B0	endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_1400018D8	proc near		; CODE XREF: sub_1400023AC+1EAp
		test	byte ptr [rcx+8], 40h
		jz	short loc_1400018EC
		mov	rax, [rcx+10h]
		movsx	rdx, word ptr [rax+1]
		add	rdx, rax
		jmp	short loc_1400018F4
; ---------------------------------------------------------------------------

loc_1400018EC:				; CODE XREF: sub_1400018D8+4j
		mov	rdx, [rcx+10h]
		add	rdx, 3

loc_1400018F4:				; CODE XREF: sub_1400018D8+12j
		mov	ecx, 681Eh
		jmp	do_vm_write
sub_1400018D8	endp

; ---------------------------------------------------------------------------
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140001900	proc near		; CODE XREF: sub_1400023AC+17Fp
					; DATA XREF: .pdata:000000014000A090o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001608
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		mov	r8d, [rbx+2]
		add	r8, [rdx+58h]
		mov	[rax], r8
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001900	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001944	proc near		; CODE XREF: sub_1400023AC+25Ap
					; DATA XREF: .pdata:000000014000A090o ...

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		mov	r9d, [rbx+2]
		mov	r8, [rdx+58h]
		mov	edx, [r9+r8]
		mov	[rax], edx
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001944	endp

; ---------------------------------------------------------------------------
algn_14000198B:				; DATA XREF: .pdata:000000014000A09Co
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000198C	proc near		; CODE XREF: sub_1400023AC+A9p
					; DATA XREF: .pdata:000000014000A0A8o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		mov	[rsp+arg_10], rdi
		push	r14
		sub	rsp, 20h
		mov	rsi, [rcx+10h]
		mov	bl, dl
		mov	r14, rcx
		lea	rdx, [rsi+1]
		call	sub_140001598
		mov	rdi, rax
		test	bl, bl
		jz	short loc_1400019C1
		mov	ebx, [rsi+2]
		add	ebx, [rax]
		jmp	short loc_1400019C6
; ---------------------------------------------------------------------------

loc_1400019C1:				; CODE XREF: sub_14000198C+2Cj
		mov	ebx, [rax]
		sub	ebx, [rsi+2]

loc_1400019C6:				; CODE XREF: sub_14000198C+33j
		mov	rax, [r14]
		add	rax, 58h
		cmp	rdi, rax
		jnz	short loc_1400019DF
		movsxd	rdx, ebx
		mov	ecx, 681Ch
		call	do_vm_write

loc_1400019DF:				; CODE XREF: sub_14000198C+44j
		mov	[rdi], ebx
		mov	ecx, 681Eh
		mov	rdx, [r14+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		mov	rdi, [rsp+28h+arg_10]
		add	rsp, 20h
		pop	r14
		jmp	do_vm_write
sub_14000198C	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001A08	proc near		; CODE XREF: sub_1400023AC+8Ep
					; DATA XREF: .pdata:000000014000A0A8o ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		mov	[rsp+arg_10], rdi
		push	r14
		sub	rsp, 20h
		mov	rsi, [rcx+10h]
		mov	bl, dl
		mov	r14, rcx
		lea	rdx, [rsi+1]
		call	sub_140001608
		mov	rdi, rax
		test	bl, bl
		jz	short loc_140001A3E
		mov	ebx, [rsi+2]
		add	rbx, [rax]
		jmp	short loc_140001A47
; ---------------------------------------------------------------------------

loc_140001A3E:				; CODE XREF: sub_140001A08+2Cj
		mov	eax, [rsi+2]
		mov	rbx, [rdi]
		sub	rbx, rax

loc_140001A47:				; CODE XREF: sub_140001A08+34j
		mov	rax, [r14]
		add	rax, 58h
		cmp	rdi, rax
		jnz	short loc_140001A60
		mov	rdx, rbx
		mov	ecx, 681Ch
		call	do_vm_write

loc_140001A60:				; CODE XREF: sub_140001A08+49j
		mov	[rdi], rbx
		mov	ecx, 681Eh
		mov	rdx, [r14+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		mov	rdi, [rsp+28h+arg_10]
		add	rsp, 20h
		pop	r14
		jmp	do_vm_write
sub_140001A08	endp

; ---------------------------------------------------------------------------
algn_140001A8A:				; DATA XREF: .pdata:000000014000A0B4o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001A8C	proc near		; CODE XREF: sub_1400023AC+C4p
					; DATA XREF: .pdata:000000014000A0C0o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rsi
		mov	[rax+18h], rdi
		mov	[rax+20h], r14
		push	r15
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	dil, dl
		mov	r14, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		lea	rdx, [rbx+2]
		mov	rcx, r14
		mov	r15, rax
		call	sub_140001598
		mov	rsi, rax
		mov	ebx, [rax]
		test	dil, dil
		jz	short loc_140001AD6
		add	ebx, [r15]
		jmp	short loc_140001AD9
; ---------------------------------------------------------------------------

loc_140001AD6:				; CODE XREF: sub_140001A8C+43j
		sub	ebx, [r15]

loc_140001AD9:				; CODE XREF: sub_140001A8C+48j
		mov	rax, [r14]
		add	rax, 58h
		cmp	rsi, rax
		jnz	short loc_140001AF1
		mov	edx, ebx
		mov	ecx, 681Ch
		call	do_vm_write

loc_140001AF1:				; CODE XREF: sub_140001A8C+57j
		mov	[rsi], ebx
		mov	ecx, 681Eh
		mov	rdx, [r14+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		mov	rdi, [rsp+28h+arg_10]
		mov	r14, [rsp+28h+arg_18]
		add	rsp, 20h
		pop	r15
		jmp	do_vm_write
sub_140001A8C	endp

; ---------------------------------------------------------------------------
algn_140001B1F:				; DATA XREF: .pdata:000000014000A0C0o
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140001B20	proc near		; CODE XREF: sub_1400023AC+26Cp
		mov	rax, [rcx+10h]
		mov	r8, [rcx]
		mov	edx, [rax+1]
		mov	rax, [r8+58h]
		mov	dl, [rdx+rax]
		mov	[r8+78h], dl
		mov	rdx, [rcx+10h]
		mov	ecx, 681Eh
		add	rdx, 5
		jmp	do_vm_write
sub_140001B20	endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140001B48	proc near		; CODE XREF: sub_1400023AC+15Dp
					; DATA XREF: .pdata:000000014000A0CCo

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001608
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		mov	r9d, [rbx+2]
		mov	r8, [rdx+58h]
		mov	rdx, [r9+r8]
		mov	[rax], rdx
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001B48	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001B90	proc near		; CODE XREF: sub_1400023AC+299p
					; DATA XREF: .pdata:000000014000A0CCo ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+2]
		call	sub_140001598
		lea	rdx, [rdi+1]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001598
		mov	ecx, 681Eh
		mov	edx, [rax]
		mov	[rbx], edx
		mov	rdx, [rsi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001B90	endp

; ---------------------------------------------------------------------------
algn_140001BE3:				; DATA XREF: .pdata:000000014000A0D8o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001BE4	proc near		; CODE XREF: sub_1400023AC+73p
					; DATA XREF: .pdata:000000014000A0E4o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+2]
		call	sub_140001608
		lea	rdx, [rdi+1]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001608
		mov	ecx, 681Eh
		mov	rdx, [rax]
		mov	[rbx], rdx
		mov	rdx, [rsi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001BE4	endp

; ---------------------------------------------------------------------------
algn_140001C39:				; DATA XREF: .pdata:000000014000A0E4o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001C3C	proc near		; CODE XREF: sub_1400023AC+108p
					; DATA XREF: .pdata:000000014000A0F0o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	edx, [rbx+2]
		mov	ecx, 681Eh
		mov	[rax], edx
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001C3C	endp

; ---------------------------------------------------------------------------
algn_140001C77:				; DATA XREF: .pdata:000000014000A0F0o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140001C78	proc near		; CODE XREF: sub_1400023AC+119p
					; DATA XREF: .pdata:000000014000A0FCo

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	rdx, [rbx+2]
		mov	ecx, 681Eh
		mov	[rax], rdx
		mov	rdx, [rdi+10h]
		add	rdx, 0Ah
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001C78	endp

; ---------------------------------------------------------------------------
algn_140001CB5:				; DATA XREF: .pdata:000000014000A0FCo
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140001CB8	proc near		; CODE XREF: sub_1400023AC+224p
					; DATA XREF: .pdata:000000014000A108o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r13
		push	r14
		push	r15
		sub	rsp, 20h
		mov	r13, [rcx+10h]
		xor	esi, esi
		mov	rbx, rcx
		mov	ebp, 6
		lea	rdi, [r13+1]
		mov	rdx, rdi
		call	sub_140001598
		mov	r15, rax
		lea	r14, [rdi+1]
		jmp	short loc_140001D0D
; ---------------------------------------------------------------------------

loc_140001CF8:				; CODE XREF: sub_140001CB8+63j
		mov	rdx, r14
		mov	rcx, rbx
		call	sub_140001608
		inc	rdi
		inc	r14
		add	esi, [rax]
		inc	ebp

loc_140001D0D:				; CODE XREF: sub_140001CB8+3Ej
		mov	rdx, r14
		mov	rcx, rbx
		call	sub_140001608
		test	rax, rax
		jnz	short loc_140001CF8
		cmp	byte ptr [r13+0], 1Fh
		jnz	short loc_140001D29
		mov	edx, [rdi+1]
		jmp	short loc_140001D36
; ---------------------------------------------------------------------------

loc_140001D29:				; CODE XREF: sub_140001CB8+6Aj
		mov	rax, [rbx]
		mov	ecx, [rdi+1]
		mov	rdx, [rax+58h]
		add	rdx, rcx

loc_140001D36:				; CODE XREF: sub_140001CB8+6Fj
		mov	eax, esi
		mov	rcx, r15
		add	rdx, rax
		call	sub_140001579
		mov	edx, ebp
		mov	ecx, 681Eh
		add	rdx, [rbx+10h]
		mov	rbx, [rsp+38h+arg_0]
		mov	rbp, [rsp+38h+arg_8]
		mov	rsi, [rsp+38h+arg_10]
		mov	rdi, [rsp+38h+arg_18]
		add	rsp, 20h
		pop	r15
		pop	r14
		pop	r13
		jmp	do_vm_write
sub_140001CB8	endp

; ---------------------------------------------------------------------------
algn_140001D71:				; DATA XREF: .pdata:000000014000A108o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001D74	proc near		; CODE XREF: sub_1400023AC+236p
					; DATA XREF: .pdata:000000014000A114o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r14
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		inc	rbx
		mov	ebp, 6
		mov	rdx, rbx
		call	sub_140001608
		mov	r14, rax
		lea	rsi, [rbx+1]
		jmp	short loc_140001DB5
; ---------------------------------------------------------------------------

loc_140001DAD:				; CODE XREF: sub_140001D74+4Fj
		inc	ebp
		mov	rbx, rsi
		inc	rsi

loc_140001DB5:				; CODE XREF: sub_140001D74+37j
		mov	rdx, rsi
		mov	rcx, rdi
		call	sub_140001608
		test	rax, rax
		jnz	short loc_140001DAD
		mov	rax, [rdi]
		mov	rcx, r14
		mov	edx, [rbx+1]
		add	rdx, [rax+58h]
		call	sub_140001580
		mov	edx, ebp
		mov	ecx, 681Eh
		add	rdx, [rdi+10h]
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		mov	rdi, [rsp+28h+arg_18]
		add	rsp, 20h
		pop	r14
		jmp	do_vm_write
sub_140001D74	endp

; ---------------------------------------------------------------------------
algn_140001E01:				; DATA XREF: .pdata:000000014000A114o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001E04	proc near		; CODE XREF: sub_1400023AC+210p
					; DATA XREF: .pdata:000000014000A120o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r13
		push	r14
		push	r15
		sub	rsp, 20h
		mov	r13, [rcx+10h]
		xor	ebp, ebp
		mov	rbx, rcx
		lea	rdi, [r13+1]
		mov	rdx, rdi
		lea	r14d, [rbp+6]
		call	sub_140001598
		mov	rsi, rax
		lea	r15, [rdi+1]
		jmp	short loc_140001E59
; ---------------------------------------------------------------------------

loc_140001E43:				; CODE XREF: sub_140001E04+63j
		mov	rdx, r15
		mov	rcx, rbx
		call	sub_140001608
		inc	rdi
		inc	r15
		add	ebp, [rax]
		inc	r14d

loc_140001E59:				; CODE XREF: sub_140001E04+3Dj
		mov	rdx, r15
		mov	rcx, rbx
		call	sub_140001608
		test	rax, rax
		jnz	short loc_140001E43
		and	[rsi], eax
		cmp	byte ptr [r13+0], 20h
		jnz	short loc_140001E7B
		mov	eax, [rdi+1]
		add	eax, ebp
		mov	ecx, [rax]
		jmp	short loc_140001E88
; ---------------------------------------------------------------------------

loc_140001E7B:				; CODE XREF: sub_140001E04+6Cj
		mov	rax, [rbx]
		mov	ecx, [rdi+1]
		add	rcx, [rax+58h]
		mov	ecx, [rcx+rbp]

loc_140001E88:				; CODE XREF: sub_140001E04+75j
		mov	[rsi], ecx
		mov	ecx, 681Eh
		mov	edx, r14d
		add	rdx, [rbx+10h]
		mov	rbx, [rsp+38h+arg_0]
		mov	rbp, [rsp+38h+arg_8]
		mov	rsi, [rsp+38h+arg_10]
		mov	rdi, [rsp+38h+arg_18]
		add	rsp, 20h
		pop	r15
		pop	r14
		pop	r13
		jmp	do_vm_write
sub_140001E04	endp

; ---------------------------------------------------------------------------
algn_140001EB9:				; DATA XREF: .pdata:000000014000A120o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001EBC	proc near		; CODE XREF: sub_1400023AC+40p
					; DATA XREF: .pdata:000000014000A12Co

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rdx, [rcx+10h]
		mov	rdi, rcx
		inc	rdx
		call	sub_140001608
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		mov	r8, [rdx+58h]
		mov	rdx, [r8]
		mov	[rax], rdx
		mov	rax, [rdi]
		add	qword ptr [rax+58h], 8
		mov	rdx, [rdi+10h]
		mov	rbx, [rax+58h]
		add	rdx, 2
		call	do_vm_write
		mov	rdx, rbx
		mov	ecx, 681Ch
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001EBC	endp

; ---------------------------------------------------------------------------
algn_140001F17:				; DATA XREF: .pdata:000000014000A12Co
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140001F18	proc near		; CODE XREF: sub_1400023AC+51p
					; DATA XREF: .pdata:000000014000A138o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rdx, [rcx+10h]
		mov	rdi, rcx
		inc	rdx
		call	sub_140001608
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		add	qword ptr [rdx+58h], 0FFFFFFFFFFFFFFF8h
		mov	rbx, [rdx+58h]
		mov	r8, [rdi]
		mov	rax, [rax]
		mov	r9, [r8+58h]
		mov	[r9], rax
		mov	rdx, [rdi+10h]
		add	rdx, 2
		call	do_vm_write
		mov	rdx, rbx
		mov	ecx, 681Ch
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001F18	endp

; ---------------------------------------------------------------------------
algn_140001F73:				; DATA XREF: .pdata:000000014000A138o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001F74	proc near		; CODE XREF: sub_1400023AC+12Ap
					; DATA XREF: .pdata:000000014000A144o
		push	rbx
		sub	rsp, 20h
		mov	rbx, rcx
		mov	rcx, [rcx]
		mov	rax, [rcx+78h]
		mov	r8, [rcx+70h]
		mov	rcx, [rcx+40h]
		movzx	edx, byte ptr [rax]
		call	init_memory
		mov	rdx, [rbx+10h]
		mov	ecx, 681Eh
		inc	rdx
		add	rsp, 20h
		pop	rbx
		jmp	do_vm_write
sub_140001F74	endp

; ---------------------------------------------------------------------------
algn_140001FAA:				; DATA XREF: .pdata:000000014000A144o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140001FAC	proc near		; CODE XREF: sub_1400023AC+2Fp
					; DATA XREF: .pdata:000000014000A150o
		push	rbx
		sub	rsp, 20h
		mov	r8, [rcx]
		mov	ecx, 681Eh
		mov	rax, [r8+58h]
		mov	rdx, [rax]
		lea	rbx, [rax+8]
		mov	[r8+58h], rbx
		call	do_vm_write
		mov	rdx, rbx
		mov	ecx, 681Ch
		add	rsp, 20h
		pop	rbx
		jmp	do_vm_write
sub_140001FAC	endp


; =============== S U B	R O U T	I N E =======================================


sub_140001FE0	proc near		; CODE XREF: sub_1400023AC+2D5p
					; DATA XREF: .pdata:000000014000A150o ...

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001608
		mov	cl, [rbx+2]
		shr	dword ptr [rax], cl
		mov	ecx, 681Eh
		mov	rdx, [rdi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140001FE0	endp

; ---------------------------------------------------------------------------
algn_14000201B:				; DATA XREF: .pdata:000000014000A15Co
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000201C	proc near		; CODE XREF: sub_1400023AC+2C6p
					; DATA XREF: .pdata:000000014000A168o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	cl, [rbx+2]
		shr	dword ptr [rax], cl
		mov	ecx, 681Eh
		mov	rdx, [rdi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_14000201C	endp

; ---------------------------------------------------------------------------
algn_140002057:				; DATA XREF: .pdata:000000014000A168o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140002058	proc near		; CODE XREF: sub_1400023AC+27Bp
		mov	r9, [rcx]
		mov	rax, [rcx+10h]
		mov	rdx, [r9+58h]
		mov	r8d, [rax+1]
		mov	al, [r9+78h]
		mov	[r8+rdx], al
		mov	rdx, [rcx+10h]
		mov	ecx, 681Eh
		add	rdx, 5
		jmp	do_vm_write
sub_140002058	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140002084	proc near		; CODE XREF: sub_1400023AC+14Cp
					; DATA XREF: .pdata:000000014000A174o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		mov	r9d, [rbx+2]
		mov	eax, [rax]
		mov	r8, [rdx+58h]
		mov	[r9+r8], eax
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140002084	endp

; ---------------------------------------------------------------------------
algn_1400020CB:				; DATA XREF: .pdata:000000014000A174o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400020CC	proc near		; CODE XREF: sub_1400023AC+13Bp
					; DATA XREF: .pdata:000000014000A180o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001608
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		mov	r9d, [rbx+2]
		mov	rax, [rax]
		mov	r8, [rdx+58h]
		mov	[r9+r8], rax
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_1400020CC	endp


; =============== S U B	R O U T	I N E =======================================


sub_140002114	proc near		; CODE XREF: sub_1400023AC+16Ep
					; DATA XREF: .pdata:000000014000A180o ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+1]
		call	sub_140001608
		lea	rdx, [rdi+2]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001608
		mov	ecx, 681Eh
		mov	rdx, [rax]
		mov	rax, [rbx]
		mov	[rdx], rax
		mov	rdx, [rsi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140002114	endp


; =============== S U B	R O U T	I N E =======================================


sub_14000216C	proc near		; CODE XREF: sub_1400023AC+D5p
					; DATA XREF: .pdata:000000014000A18Co
		mov	r9, [rcx+10h]
		mov	rax, [rcx]
		mov	r8d, [r9+1]
		mov	rdx, [rax+58h]
		mov	rax, [r9+5]
		mov	[r8+rdx], rax
		mov	rdx, [rcx+10h]
		mov	ecx, 681Eh
		add	rdx, 0Dh
		jmp	do_vm_write
sub_14000216C	endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140002198	proc near		; CODE XREF: sub_1400023AC+190p
					; DATA XREF: .pdata:000000014000A198o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+2]
		call	sub_140001598
		lea	rdx, [rdi+1]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001598
		mov	rdx, [rax]
		test	[rbx], rdx
		jnz	short loc_1400021D5
		or	qword ptr [rsi+8], 40h
		jmp	short loc_1400021DA
; ---------------------------------------------------------------------------

loc_1400021D5:				; CODE XREF: sub_140002198+34j
		and	qword ptr [rsi+8], 0FFFFFFFFFFFFFFBFh

loc_1400021DA:				; CODE XREF: sub_140002198+3Bj
		mov	rdx, [rsi+8]
		mov	ecx, 6820h
		call	do_vm_write
		mov	rdx, [rsi+10h]
		mov	ecx, 681Eh
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140002198	endp

; ---------------------------------------------------------------------------
algn_140002209:				; DATA XREF: .pdata:000000014000A198o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000220C	proc near		; CODE XREF: sub_1400023AC+2A8p
					; DATA XREF: .pdata:000000014000A1A4o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+2]
		call	sub_140001608
		lea	rdx, [rdi+1]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001608
		mov	edx, [rax]
		test	[rbx], edx
		jnz	short loc_140002247
		or	qword ptr [rsi+8], 40h
		jmp	short loc_14000224C
; ---------------------------------------------------------------------------

loc_140002247:				; CODE XREF: sub_14000220C+32j
		and	qword ptr [rsi+8], 0FFFFFFFFFFFFFFBFh

loc_14000224C:				; CODE XREF: sub_14000220C+39j
		mov	rdx, [rsi+8]
		mov	ecx, 6820h
		call	do_vm_write
		mov	rdx, [rsi+10h]
		mov	ecx, 681Eh
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_14000220C	endp

; ---------------------------------------------------------------------------
algn_14000227B:				; DATA XREF: .pdata:000000014000A1A4o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000227C	proc near		; CODE XREF: sub_1400023AC+248p
					; DATA XREF: .pdata:000000014000A1B0o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	rdx, [rdi]
		mov	ecx, 681Eh
		mov	r9d, [rbx+2]
		mov	r8, [rdx+58h]
		mov	edx, [r9+r8]
		xor	[rax], edx
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_14000227C	endp

; ---------------------------------------------------------------------------
algn_1400022C3:				; DATA XREF: .pdata:000000014000A1B0o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400022C4	proc near		; CODE XREF: sub_1400023AC+28Ap
					; DATA XREF: .pdata:000000014000A1BCo

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, [rcx+10h]
		mov	rdi, rcx
		lea	rdx, [rbx+1]
		call	sub_140001598
		mov	edx, [rbx+2]
		mov	ecx, 681Eh
		xor	[rax], edx
		mov	rdx, [rdi+10h]
		add	rdx, 6
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_1400022C4	endp

; ---------------------------------------------------------------------------
algn_1400022FF:				; DATA XREF: .pdata:000000014000A1BCo
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140002300	proc near		; CODE XREF: sub_1400023AC+E6p
					; DATA XREF: .pdata:000000014000A1C8o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+1]
		call	sub_140001598
		lea	rdx, [rdi+2]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001598
		mov	ecx, 681Eh
		mov	edx, [rax]
		xor	[rbx], edx
		mov	rdx, [rsi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140002300	endp

; ---------------------------------------------------------------------------
algn_140002353:				; DATA XREF: .pdata:000000014000A1C8o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140002354	proc near		; CODE XREF: sub_1400023AC+F7p
					; DATA XREF: .pdata:000000014000A1D4o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, [rcx+10h]
		mov	rsi, rcx
		lea	rdx, [rdi+2]
		call	sub_140001608
		lea	rdx, [rdi+1]
		mov	rcx, rsi
		mov	rbx, rax
		call	sub_140001608
		mov	ecx, 681Eh
		mov	rdx, [rax]
		xor	[rbx], rdx
		mov	rdx, [rsi+10h]
		add	rdx, 3
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	do_vm_write
sub_140002354	endp

; ---------------------------------------------------------------------------
algn_1400023A9:				; DATA XREF: .pdata:000000014000A1D4o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400023AC	proc near		; CODE XREF: real_handler+274p
					; DATA XREF: .pdata:000000014000A1E0o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, rcx
		mov	ecx, 6802h
		call	do_vm_read
		mov	rdi, cr3
		mov	[rsp+28h+arg_8], rdi

loc_1400023CB:				; DATA XREF: .rdata:0000000140006570o
		mov	cr3, rax
		mov	rcx, [rbx+10h]
		mov	al, [rcx]
		cmp	al, 1
		jnz	short loc_1400023E5
		mov	rcx, rbx
		call	sub_140001FAC
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400023E5:				; CODE XREF: sub_1400023AC+2Aj
		cmp	al, 0BBh
		jnz	short loc_1400023F6
		mov	rcx, rbx
		call	sub_140001EBC
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400023F6:				; CODE XREF: sub_1400023AC+3Bj
		cmp	al, 0AAh
		jnz	short loc_140002407
		mov	rcx, rbx
		call	sub_140001F18
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002407:				; CODE XREF: sub_1400023AC+4Cj
		cmp	al, 0C2h
		jnz	short loc_140002418
		mov	rcx, rbx
		call	sub_1400016EC
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002418:				; CODE XREF: sub_1400023AC+5Dj
		test	al, al
		jnz	short loc_140002429
		mov	rcx, rbx
		call	sub_140001BE4
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002429:				; CODE XREF: sub_1400023AC+6Ej
		cmp	al, 0C3h
		jnz	short loc_140002431
		xor	edx, edx
		jmp	short loc_140002437
; ---------------------------------------------------------------------------

loc_140002431:				; CODE XREF: sub_1400023AC+7Fj
		cmp	al, 0C1h
		jnz	short loc_140002444
		mov	dl, 1

loc_140002437:				; CODE XREF: sub_1400023AC+83j
		mov	rcx, rbx
		call	sub_140001A08
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002444:				; CODE XREF: sub_1400023AC+87j
		cmp	al, 0D1h
		jnz	short loc_14000244C
		mov	dl, 1
		jmp	short loc_140002452
; ---------------------------------------------------------------------------

loc_14000244C:				; CODE XREF: sub_1400023AC+9Aj
		cmp	al, 0D3h
		jnz	short loc_14000245F
		xor	edx, edx

loc_140002452:				; CODE XREF: sub_1400023AC+9Ej
		mov	rcx, rbx
		call	sub_14000198C
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_14000245F:				; CODE XREF: sub_1400023AC+A2j
		cmp	al, 0D2h
		jnz	short loc_140002467
		mov	dl, 1
		jmp	short loc_14000246D
; ---------------------------------------------------------------------------

loc_140002467:				; CODE XREF: sub_1400023AC+B5j
		cmp	al, 0D4h
		jnz	short loc_14000247A
		xor	edx, edx

loc_14000246D:				; CODE XREF: sub_1400023AC+B9j
		mov	rcx, rbx
		call	sub_140001A8C
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_14000247A:				; CODE XREF: sub_1400023AC+BDj
		cmp	al, 0C9h
		jnz	short loc_14000248B
		mov	rcx, rbx
		call	sub_14000216C
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_14000248B:				; CODE XREF: sub_1400023AC+D0j
		cmp	al, 0D5h
		jnz	short loc_14000249C
		mov	rcx, rbx
		call	sub_140002300
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_14000249C:				; CODE XREF: sub_1400023AC+E1j
		cmp	al, 0C5h
		jnz	short loc_1400024AD
		mov	rcx, rbx
		call	sub_140002354
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400024AD:				; CODE XREF: sub_1400023AC+F2j
		cmp	al, 0D6h
		jnz	short loc_1400024BE
		mov	rcx, rbx
		call	sub_140001C3C
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400024BE:				; CODE XREF: sub_1400023AC+103j
		cmp	al, 0C6h
		jnz	short loc_1400024CF
		mov	rcx, rbx
		call	sub_140001C78
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400024CF:				; CODE XREF: sub_1400023AC+114j
		cmp	al, 30h
		jnz	short loc_1400024E0
		mov	rcx, rbx
		call	sub_140001F74
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400024E0:				; CODE XREF: sub_1400023AC+125j
		cmp	al, 0C8h
		jnz	short loc_1400024F1
		mov	rcx, rbx
		call	sub_1400020CC
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400024F1:				; CODE XREF: sub_1400023AC+136j
		cmp	al, 0D8h
		jnz	short loc_140002502
		mov	rcx, rbx
		call	sub_140002084
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002502:				; CODE XREF: sub_1400023AC+147j
		cmp	al, 1Ah
		jnz	short loc_140002513
		mov	rcx, rbx
		call	sub_140001B48
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002513:				; CODE XREF: sub_1400023AC+158j
		cmp	al, 0C7h
		jnz	short loc_140002524
		mov	rcx, rbx
		call	sub_140002114
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002524:				; CODE XREF: sub_1400023AC+169j
		cmp	al, 4Ah
		jnz	short loc_140002535
		mov	rcx, rbx
		call	sub_140001900
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002535:				; CODE XREF: sub_1400023AC+17Aj
		cmp	al, 44h
		jnz	short loc_140002546
		mov	rcx, rbx
		call	sub_140002198
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002546:				; CODE XREF: sub_1400023AC+18Bj
		cmp	al, 40h
		jnz	short loc_140002557
		mov	rcx, rbx
		call	sub_140001818
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002557:				; CODE XREF: sub_1400023AC+19Cj
		cmp	al, 42h
		jnz	short loc_140002568
		mov	rcx, rbx
		call	sub_140001780
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002568:				; CODE XREF: sub_1400023AC+1ADj
		mov	cl, [rcx]
		cmp	cl, 50h
		jnz	short loc_14000257C
		mov	rcx, rbx
		call	sub_1400016D4
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_14000257C:				; CODE XREF: sub_1400023AC+1C1j
		cmp	cl, 51h
		jnz	short loc_14000258E
		mov	rcx, rbx
		call	sub_1400018B0
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_14000258E:				; CODE XREF: sub_1400023AC+1D3j
		cmp	cl, 52h
		jnz	short loc_1400025A0
		mov	rcx, rbx
		call	sub_1400018D8
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400025A0:				; CODE XREF: sub_1400023AC+1E5j
		cmp	cl, 54h
		jnz	short loc_1400025B2
		mov	rcx, rbx
		call	sub_140001880
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400025B2:				; CODE XREF: sub_1400023AC+1F7j
		lea	eax, [rcx-1Ch]
		test	al, 0FBh
		jnz	short loc_1400025C6
		mov	rcx, rbx
		call	sub_140001E04
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400025C6:				; CODE XREF: sub_1400023AC+20Bj
		lea	eax, [rcx-1Eh]
		cmp	al, 1
		ja	short loc_1400025DA
		mov	rcx, rbx
		call	sub_140001CB8
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400025DA:				; CODE XREF: sub_1400023AC+21Fj
		cmp	cl, 1Dh
		jnz	short loc_1400025EC
		mov	rcx, rbx
		call	sub_140001D74
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400025EC:				; CODE XREF: sub_1400023AC+231j
		cmp	cl, 0D7h
		jnz	short loc_1400025FE
		mov	rcx, rbx
		call	sub_14000227C
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_1400025FE:				; CODE XREF: sub_1400023AC+243j
		cmp	cl, 19h
		jnz	short loc_140002610
		mov	rcx, rbx
		call	sub_140001944
		jmp	loc_140002698
; ---------------------------------------------------------------------------

loc_140002610:				; CODE XREF: sub_1400023AC+255j
		cmp	cl, 1Bh
		jnz	short loc_14000261F
		mov	rcx, rbx
		call	sub_140001B20
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_14000261F:				; CODE XREF: sub_1400023AC+267j
		cmp	cl, 17h
		jnz	short loc_14000262E
		mov	rcx, rbx
		call	sub_140002058
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_14000262E:				; CODE XREF: sub_1400023AC+276j
		cmp	cl, 0C0h
		jnz	short loc_14000263D
		mov	rcx, rbx
		call	sub_1400022C4
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_14000263D:				; CODE XREF: sub_1400023AC+285j
		cmp	cl, 2
		jnz	short loc_14000264C
		mov	rcx, rbx
		call	sub_140001B90
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_14000264C:				; CODE XREF: sub_1400023AC+294j
		cmp	cl, 43h
		jnz	short loc_14000265B
		mov	rcx, rbx
		call	sub_14000220C
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_14000265B:				; CODE XREF: sub_1400023AC+2A3j
		cmp	cl, 0BEh
		jnz	short loc_14000266A
		mov	rcx, rbx
		call	sub_140001744
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_14000266A:				; CODE XREF: sub_1400023AC+2B2j
		cmp	cl, 0BCh
		jnz	short loc_140002679
		mov	rcx, rbx
		call	sub_14000201C
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_140002679:				; CODE XREF: sub_1400023AC+2C1j
		cmp	cl, 0B9h
		jnz	short loc_140002688
		mov	rcx, rbx
		call	sub_140001FE0
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_140002688:				; CODE XREF: sub_1400023AC+2D0j
		cmp	cl, 41h
		jnz	short loc_140002697
		mov	rcx, rbx
		call	sub_1400017C8
		jmp	short loc_140002698
; ---------------------------------------------------------------------------

loc_140002697:				; CODE XREF: sub_1400023AC+2DFj
		int	3		; Trap to Debugger

loc_140002698:				; CODE XREF: sub_1400023AC+34j
					; sub_1400023AC+45j ...
		mov	cr3, rdi
		xor	eax, eax
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
sub_1400023AC	endp


; =============== S U B	R O U T	I N E =======================================


sub_1400026A8	proc near		; CODE XREF: sub_14000BE30+313p
					; DATA XREF: .pdata:000000014000A1E0o
		mov	rax, [rcx]
		mov	rax, [rax]
		retn
sub_1400026A8	endp

; ---------------------------------------------------------------------------
		align 10h

; =============== S U B	R O U T	I N E =======================================


compute_stuff1	proc near		; CODE XREF: VMCALL_HANDLER+A5p
					; VMCALL_HANDLER+AB8p ...
		mov	rcx, [rcx+8]
		mov	r8, rdx
		mov	edx, 4
		jmp	sub_140002AE0	; rcx :	weird initialized stuff
compute_stuff1	endp			;

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400026C4	proc near		; CODE XREF: real_handler+254p
					; DATA XREF: .pdata:000000014000A1ECo

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r14
		sub	rsp, 20h
		mov	rsi, rcx
		xor	edi, edi
		mov	ecx, 6400h
		call	do_vm_read
		mov	ecx, 2400h
		mov	rbx, rax
		call	do_vm_read
		mov	dl, bl
		lea	r14d, [rdi+4]
		and	dl, 24h
		mov	rbp, rax
		cmp	dl, r14b
		jnz	short loc_140002713
		lea	edi, [r14-3]
		jmp	loc_1400027A1
; ---------------------------------------------------------------------------

loc_140002713:				; CODE XREF: sub_1400026C4+44j
		mov	al, bl
		and	al, 12h
		cmp	al, 2
		jnz	short loc_14000273B
		mov	rcx, [rsi+8]
		mov	r8, rbp
		mov	edx, r14d
		call	sub_140002AE0	; rcx :	weird initialized stuff
					;
		test	rax, rax
		jz	short loc_14000278F
		cmp	[rax], rdi
		jz	short loc_14000278F
		mov	eax, 2
		jmp	short loc_1400027A8
; ---------------------------------------------------------------------------

loc_14000273B:				; CODE XREF: sub_1400026C4+55j
		test	bl, 1
		jz	short loc_140002765
		test	bl, 8
		jnz	short loc_140002765
		mov	rcx, [rsi+8]
		mov	r8, rbp
		mov	edx, r14d
		call	sub_140002AE0	; rcx :	weird initialized stuff
					;
		test	rax, rax
		jz	short loc_14000278F
		cmp	[rax], rdi
		jz	short loc_14000278F
		mov	eax, 3
		jmp	short loc_1400027A8
; ---------------------------------------------------------------------------

loc_140002765:				; CODE XREF: sub_1400026C4+7Aj
					; sub_1400026C4+7Fj
		mov	rcx, [rsi+8]
		mov	r8, rbp
		mov	edx, r14d
		call	sub_140002AE0	; rcx :	weird initialized stuff
					;
		test	rax, rax
		jz	short loc_14000278F
		cmp	[rax], rdi
		jz	short loc_14000278F
		mov	rax, cs:KdDebuggerNotPresent
		cmp	[rax], dil
		jnz	short loc_14000278B
		int	3		; Trap to Debugger

loc_14000278B:				; CODE XREF: sub_1400026C4+C4j
		xor	eax, eax
		jmp	short loc_1400027A8
; ---------------------------------------------------------------------------

loc_14000278F:				; CODE XREF: sub_1400026C4+69j
					; sub_1400026C4+6Ej ...
		mov	rcx, [rsi+8]
		mov	r9, rsi
		mov	r8, rbp
		mov	edx, r14d
		call	sub_140002870

loc_1400027A1:				; CODE XREF: sub_1400026C4+4Aj
		call	sub_140002D30
		mov	eax, edi

loc_1400027A8:				; CODE XREF: sub_1400026C4+75j
					; sub_1400026C4+9Fj ...
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		mov	rdi, [rsp+28h+arg_18]
		add	rsp, 20h
		pop	r14
		retn
sub_1400026C4	endp

; ---------------------------------------------------------------------------
algn_1400027C3:				; DATA XREF: .pdata:000000014000A1ECo
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400027C4	proc near		; CODE XREF: sub_14000B950+54p
					; DATA XREF: .pdata:000000014000A1F8o
		push	rbx
		sub	rsp, 20h
		mov	edx, [rcx+18h]
		mov	rbx, rcx
		mov	rcx, [rcx+10h]
		call	sub_140002A84
		mov	rcx, [rbx+8]
		mov	edx, 4
		call	sub_1400029E4
		mov	rcx, [rbx]	; P
		mov	edx, 56484C46h	; Tag
		call	cs:ExFreePoolWithTag
		mov	edx, 56484C46h
		mov	rcx, rbx
		add	rsp, 20h
		pop	rbx
		jmp	cs:ExFreePoolWithTag
sub_1400027C4	endp

; ---------------------------------------------------------------------------
algn_140002809:				; DATA XREF: .pdata:000000014000A1F8o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000280C	proc near		; CODE XREF: sub_140002870+67p
					; sub_140002870+BBp ...

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		xor	ebx, ebx
		test	rcx, rcx
		jz	short loc_140002832
		lea	eax, [rbx+1]
		lock xadd [rcx+18h], eax
		movsxd	rdx, eax
		mov	rax, [rcx+10h]
		mov	rax, [rax+rdx*8]
		jmp	short loc_140002863
; ---------------------------------------------------------------------------

loc_140002832:				; CODE XREF: sub_14000280C+Fj
		mov	edx, 1000h	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		mov	r8d, 56484C46h	; Tag
		call	cs:ExAllocatePoolWithTag
		mov	rdi, rax
		test	rax, rax
		jz	short loc_140002860
		xor	edx, edx
		mov	r8d, 1000h
		mov	rcx, rax
		call	init_memory
		mov	rbx, rdi

loc_140002860:				; CODE XREF: sub_14000280C+3Fj
		mov	rax, rbx

loc_140002863:				; CODE XREF: sub_14000280C+24j
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
sub_14000280C	endp

; ---------------------------------------------------------------------------
algn_14000286E:				; DATA XREF: .pdata:000000014000A204o
		align 10h

; =============== S U B	R O U T	I N E =======================================


sub_140002870	proc near		; CODE XREF: sub_1400026C4+D8p
					; init_CSTRUCT_0x20+128p ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		mov	[rsp+arg_10], rsi
		push	rdi
		push	r12
		push	r15
		sub	rsp, 20h
		mov	rbp, r9
		mov	rdi, r8
		mov	ebx, edx
		mov	r15d, 1FFh
		mov	r12, 0FFFFFFFFFh

loc_1400028A0:				; CODE XREF: sub_140002870+A2j
		sub	ebx, 1
		jz	loc_1400029A8
		sub	ebx, 1
		jz	loc_140002954
		sub	ebx, 1
		jz	short loc_140002914
		cmp	ebx, 1
		jnz	loc_140002997
		mov	rax, rdi
		shr	rax, 27h
		and	rax, r15
		lea	rsi, [rcx+rax*8]
		cmp	qword ptr [rsi], 0
		jnz	short loc_1400028FB
		mov	rcx, rbp
		call	sub_14000280C
		test	rax, rax
		jz	loc_1400029A4
		mov	rcx, rax
		call	MmGetPhysicalAddress
		mov	r8, rax
		lea	edx, [rbx+3]
		mov	rcx, rsi
		call	sub_140002C58

loc_1400028FB:				; CODE XREF: sub_140002870+62j
		mov	ebx, 3

loc_140002900:				; CODE XREF: sub_140002870+E2j
					; sub_140002870+122j
		mov	rcx, [rsi]
		shr	rcx, 0Ch
		and	rcx, r12
		call	sub_140002F8C
		mov	rcx, rax
		jmp	short loc_1400028A0
; ---------------------------------------------------------------------------

loc_140002914:				; CODE XREF: sub_140002870+45j
		mov	rax, rdi
		shr	rax, 1Eh
		and	rax, r15
		lea	rsi, [rcx+rax*8]
		cmp	qword ptr [rsi], 0
		jnz	short loc_14000294D
		mov	rcx, rbp
		call	sub_14000280C
		test	rax, rax
		jz	short loc_1400029A4
		mov	rcx, rax
		call	MmGetPhysicalAddress
		mov	r8, rax
		mov	edx, 3
		mov	rcx, rsi
		call	sub_140002C58

loc_14000294D:				; CODE XREF: sub_140002870+B6j
		mov	ebx, 2
		jmp	short loc_140002900
; ---------------------------------------------------------------------------

loc_140002954:				; CODE XREF: sub_140002870+3Cj
		mov	rax, rdi
		shr	rax, 15h
		and	rax, r15
		lea	rsi, [rcx+rax*8]
		cmp	qword ptr [rsi], 0
		jnz	short loc_14000298D
		mov	rcx, rbp
		call	sub_14000280C
		test	rax, rax
		jz	short loc_1400029A4
		mov	rcx, rax
		call	MmGetPhysicalAddress
		mov	r8, rax
		mov	edx, 2
		mov	rcx, rsi
		call	sub_140002C58

loc_14000298D:				; CODE XREF: sub_140002870+F6j
		mov	ebx, 1
		jmp	loc_140002900
; ---------------------------------------------------------------------------

loc_140002997:				; CODE XREF: sub_140002870+4Aj
		mov	rax, cs:KdDebuggerNotPresent
		cmp	byte ptr [rax],	0
		jnz	short loc_1400029A4
		int	3		; Trap to Debugger

loc_1400029A4:				; CODE XREF: sub_140002870+6Fj
					; sub_140002870+C3j ...
		xor	eax, eax
		jmp	short loc_1400029C9
; ---------------------------------------------------------------------------

loc_1400029A8:				; CODE XREF: sub_140002870+33j
		mov	rax, rdi
		mov	r8, rdi
		shr	rax, 0Ch
		mov	edx, 1
		and	rax, r15
		lea	rbx, [rcx+rax*8]
		mov	rcx, rbx
		call	sub_140002C58
		mov	rax, rbx

loc_1400029C9:				; CODE XREF: sub_140002870+136j
		mov	rbx, [rsp+38h+arg_0]
		mov	rbp, [rsp+38h+arg_8]
		mov	rsi, [rsp+38h+arg_10]
		add	rsp, 20h
		pop	r15
		pop	r12
		pop	rdi
		retn
sub_140002870	endp

; ---------------------------------------------------------------------------
algn_1400029E2:				; DATA XREF: .pdata:000000014000A210o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400029E4	proc near		; CODE XREF: sub_1400027C4+1Ep
					; sub_1400029E4+4Fp ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		mov	[rsp+arg_10], rsi
		push	rdi
		sub	rsp, 20h
		mov	edi, edx
		mov	rbp, rcx
		mov	rbx, rcx
		mov	esi, 200h

loc_140002A05:				; CODE XREF: sub_1400029E4+7Bj
		mov	rcx, [rbx]
		mov	rax, 0FFFFFFFFFh
		shr	rcx, 0Ch
		and	rcx, rax
		jz	short loc_140002A57
		call	sub_140002F8C
		cmp	edi, 2
		jz	short loc_140002A49
		lea	ecx, [rdi-3]
		cmp	ecx, 1
		ja	short loc_140002A3A
		lea	edx, [rdi-1]
		mov	rcx, rax
		call	sub_1400029E4
		jmp	short loc_140002A57
; ---------------------------------------------------------------------------

loc_140002A3A:				; CODE XREF: sub_1400029E4+47j
		mov	rax, cs:KdDebuggerNotPresent
		cmp	byte ptr [rax],	0
		jnz	short loc_140002A57
		int	3		; Trap to Debugger
		jmp	short loc_140002A57
; ---------------------------------------------------------------------------

loc_140002A49:				; CODE XREF: sub_1400029E4+3Fj
		mov	edx, 56484C46h	; Tag
		mov	rcx, rax	; P
		call	cs:ExFreePoolWithTag

loc_140002A57:				; CODE XREF: sub_1400029E4+35j
					; sub_1400029E4+54j ...
		add	rbx, 8
		sub	rsi, 1
		jnz	short loc_140002A05
		mov	edx, 56484C46h
		mov	rcx, rbp
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		add	rsp, 20h
		pop	rdi
		jmp	cs:ExFreePoolWithTag
sub_1400029E4	endp


; =============== S U B	R O U T	I N E =======================================


sub_140002A84	proc near		; CODE XREF: sub_1400027C4+10p
					; init_CSTRUCT_0x20+209p
					; DATA XREF: ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		movsxd	rbx, edx
		mov	rsi, rcx
		cmp	ebx, 32h
		jge	short loc_140002AC0
		lea	rdi, [rcx+rbx*8]

loc_140002AA2:				; CODE XREF: sub_140002A84+3Aj
		mov	rcx, [rdi]	; P
		test	rcx, rcx
		jz	short loc_140002AC0
		mov	edx, 56484C46h	; Tag
		call	cs:ExFreePoolWithTag
		inc	ebx
		add	rdi, 8
		cmp	ebx, 32h
		jl	short loc_140002AA2

loc_140002AC0:				; CODE XREF: sub_140002A84+18j
					; sub_140002A84+24j
		mov	edx, 56484C46h
		mov	rcx, rsi
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	cs:ExFreePoolWithTag
sub_140002A84	endp

; ---------------------------------------------------------------------------
algn_140002ADE:				; DATA XREF: .pdata:000000014000A228o
		align 20h

; =============== S U B	R O U T	I N E =======================================

; rcx :	weird initialized stuff
;

; unsigned __int64 __fastcall sub_140002AE0(__int64 weird_init,	signed int const_4, unsigned __int64 dest_buf)
sub_140002AE0	proc near		; CODE XREF: compute_stuff1+Cj
					; sub_1400026C4+61p ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		mov	[rsp+arg_10], rsi
		push	rdi
		sub	rsp, 20h
		mov	rdi, r8
		mov	ebx, edx
		test	rcx, rcx
		jz	loc_140002B89
		mov	esi, 1FFh
		mov	rbp, 0FFFFFFFFFh

loc_140002B11:				; CODE XREF: sub_140002AE0+A7j
		sub	ebx, 1
		jz	loc_140002BAF
		sub	ebx, 1
		jz	short loc_140002B5D
		sub	ebx, 1
		jz	short loc_140002B43
		cmp	ebx, 1
		jnz	short loc_140002BA0
		mov	rax, rdi
		shr	rax, 27h
		and	rax, rsi
		mov	rcx, [rcx+rax*8]
		test	rcx, rcx
		jz	short loc_140002B89
		mov	ebx, 3
		jmp	short loc_140002B75
; ---------------------------------------------------------------------------

loc_140002B43:				; CODE XREF: sub_140002AE0+42j
		mov	rax, rdi
		shr	rax, 1Eh
		and	rax, rsi
		mov	rcx, [rcx+rax*8]
		test	rcx, rcx
		jz	short loc_140002B89
		mov	ebx, 2
		jmp	short loc_140002B75
; ---------------------------------------------------------------------------

loc_140002B5D:				; CODE XREF: sub_140002AE0+3Dj
		mov	rax, rdi
		shr	rax, 15h
		and	rax, rsi
		mov	rcx, [rcx+rax*8]
		test	rcx, rcx
		jz	short loc_140002B89
		mov	ebx, 1

loc_140002B75:				; CODE XREF: sub_140002AE0+61j
					; sub_140002AE0+7Bj
		shr	rcx, 0Ch
		and	rcx, rbp
		call	sub_140002F8C
		mov	rcx, rax
		test	rax, rax
		jnz	short loc_140002B11

loc_140002B89:				; CODE XREF: sub_140002AE0+1Cj
					; sub_140002AE0+5Aj ...
		xor	eax, eax

loc_140002B8B:				; CODE XREF: sub_140002AE0+DAj
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		add	rsp, 20h
		pop	rdi
		retn
; ---------------------------------------------------------------------------

loc_140002BA0:				; CODE XREF: sub_140002AE0+47j
		mov	rax, cs:KdDebuggerNotPresent
		cmp	byte ptr [rax],	0
		jnz	short loc_140002B89
		int	3		; Trap to Debugger
		jmp	short loc_140002B89
; ---------------------------------------------------------------------------

loc_140002BAF:				; CODE XREF: sub_140002AE0+34j
		shr	rdi, 0Ch
		and	rdi, rsi
		lea	rax, [rcx+rdi*8]
		jmp	short loc_140002B8B
sub_140002AE0	endp


; =============== S U B	R O U T	I N E =======================================


sub_140002BBC	proc near		; CODE XREF: sub_140002C58+59p
					; init_CSTRUCT_0x20+A9p
					; DATA XREF: ...

var_28		= xmmword ptr -28h
var_18		= qword	ptr -18h

		sub	rsp, 28h
		mov	r9, rcx
		lea	r8, unk_140007330
		mov	dl, 0FFh

loc_140002BCC:				; CODE XREF: sub_140002BBC+76j
		movups	xmm2, xmmword ptr [r8]
		movsd	xmm1, qword ptr	[r8+10h]
		movd	eax, xmm2
		movups	[rsp+28h+var_28], xmm2
		movsd	[rsp+28h+var_18], xmm1
		test	al, al
		jz	short loc_140002C43
		cmp	qword ptr [rsp+28h+var_28+8], r9
		ja	short loc_140002C22
		cmp	r9, [rsp+28h+var_18]
		ja	short loc_140002C22
		mov	rcx, qword ptr [rsp+28h+var_28]
		mov	rax, rcx
		shr	rax, 8
		test	al, al
		jnz	short loc_140002C3D
		mov	rax, rcx
		shr	rax, 10h
		test	al, al
		jz	short loc_140002C34
		cmp	dl, 4
		jz	short loc_140002C19
		cmp	al, 4
		jnz	short loc_140002C20

loc_140002C19:				; CODE XREF: sub_140002BBC+57j
		cmp	dl, 6
		mov	dl, 4
		jz	short loc_140002C22

loc_140002C20:				; CODE XREF: sub_140002BBC+5Bj
		mov	dl, al

loc_140002C22:				; CODE XREF: sub_140002BBC+31j
					; sub_140002BBC+38j ...
		add	r8, 18h
		lea	rax, byte_140008C20
		cmp	r8, rax
		jz	short loc_140002C43
		jmp	short loc_140002BCC
; ---------------------------------------------------------------------------

loc_140002C34:				; CODE XREF: sub_140002BBC+52j
		mov	rdx, rcx
		shr	rdx, 10h
		jmp	short loc_140002C43
; ---------------------------------------------------------------------------

loc_140002C3D:				; CODE XREF: sub_140002BBC+47j
		shr	rcx, 10h
		mov	dl, cl

loc_140002C43:				; CODE XREF: sub_140002BBC+2Aj
					; sub_140002BBC+74j ...
		movzx	ecx, cs:byte_140008C20
		cmp	dl, 0FFh
		movzx	eax, dl
		cmovz	eax, ecx
		add	rsp, 28h
		retn
sub_140002BBC	endp


; =============== S U B	R O U T	I N E =======================================


sub_140002C58	proc near		; CODE XREF: sub_140002870+86p
					; sub_140002870+D8p ...

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	eax, 1
		mov	rbx, rcx
		mov	rdi, r8
		mov	esi, edx
		lea	ecx, [rax+1]

loc_140002C77:				; CODE XREF: sub_140002C58+29j
		or	[rbx], rax
		inc	rax
		sub	rcx, 1
		jnz	short loc_140002C77
		or	qword ptr [rbx], 4
		mov	rcx, rdi
		call	sub_140002F78
		shl	rax, 0Ch
		mov	rcx, 0FFFFFFFFF000h
		xor	rax, [rbx]
		and	rax, rcx
		xor	[rbx], rax
		mov	r11, [rbx]
		cmp	esi, 1
		jnz	short loc_140002CCB
		mov	rcx, rdi
		call	sub_140002BBC
		movzx	r10d, al
		shl	r10, 3
		xor	r10, r11
		and	r10d, 38h
		xor	r10, r11
		mov	[rbx], r10

loc_140002CCB:				; CODE XREF: sub_140002C58+54j
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		retn
sub_140002C58	endp

; ---------------------------------------------------------------------------
algn_140002CDB:				; DATA XREF: .pdata:000000014000A24Co
		align 4

; =============== S U B	R O U T	I N E =======================================


INIT_HOST_RSP	proc near		; CODE XREF: gogolaunch+73p
					; DATA XREF: .pdata:000000014000A258o

var_18		= dword	ptr -18h
var_10		= dword	ptr -10h

		sub	rsp, 38h
		mov	r10, cs:nm_allocate_contiguous_node_mem
		or	rax, 0FFFFFFFFFFFFFFFFh
		test	r10, r10
		jz	short loc_140002D10
		xor	edx, edx
		mov	[rsp+38h+var_10], 80000000h
		xor	r9d, r9d
		mov	[rsp+38h+var_18], 4
		mov	r8, rax
		call	r10 ; nm_allocate_contiguous_node_mem
		add	rsp, 38h
		retn
; ---------------------------------------------------------------------------

loc_140002D10:				; CODE XREF: INIT_HOST_RSP+12j
		mov	rdx, rax
		add	rsp, 38h
		jmp	cs:MmAllocateContiguousMemory
INIT_HOST_RSP	endp

; ---------------------------------------------------------------------------
algn_140002D1E:				; DATA XREF: .pdata:000000014000A258o
		align 20h
; [00000007 BYTES: COLLAPSED FUNCTION MmFreeContiguousMemory. PRESS CTRL-NUMPAD+ TO EXPAND]
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140002D28	proc near		; CODE XREF: init_CSTRUCT_0x20+EEp
		mov	rax, cs:P
		retn
sub_140002D28	endp


; =============== S U B	R O U T	I N E =======================================


sub_140002D30	proc near		; CODE XREF: sub_1400026C4:loc_1400027A1p
					; VM_ENTRY_HANDLER+68p	...

var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
var_18		= qword	ptr -18h

		sub	rsp, 48h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+48h+var_18], rax
		xor	eax, eax
		lea	rdx, [rsp+48h+var_28]
		mov	[rsp+48h+var_28], rax
		mov	[rsp+48h+var_20], rax
		lea	ecx, [rax+2]
		call	sub_14000153A
		mov	rcx, [rsp+48h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		add	rsp, 48h
		retn
sub_140002D30	endp

; ---------------------------------------------------------------------------
algn_140002D6E:				; DATA XREF: .pdata:000000014000A264o
		align 10h

; =============== S U B	R O U T	I N E =======================================


sub_140002D70	proc near		; CODE XREF: VM_ENTRY_HANDLER+6Dp
					; sub_140003144:loc_140003212p	...

var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
var_18		= qword	ptr -18h

		sub	rsp, 48h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+48h+var_18], rax
		xor	eax, eax
		lea	rdx, [rsp+48h+var_28]
		mov	[rsp+48h+var_28], rax
		mov	[rsp+48h+var_20], rax
		lea	ecx, [rax+2]
		call	some_invpid
		mov	rcx, [rsp+48h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		add	rsp, 48h
		retn
sub_140002D70	endp

; ---------------------------------------------------------------------------
algn_140002DAE:				; DATA XREF: .pdata:000000014000A270o
		align 10h

; =============== S U B	R O U T	I N E =======================================


invpid_wrap	proc near		; CODE XREF: real_handler+7Fp
					; DATA XREF: .pdata:000000014000A27Co

var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
var_18		= qword	ptr -18h

		sub	rsp, 48h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+48h+var_18], rax
		xor	eax, eax
		mov	[rsp+48h+var_20], rdx
		mov	[rsp+48h+var_28], rax
		lea	rdx, [rsp+48h+var_28]
		mov	word ptr [rsp+48h+var_28], cx
		xor	ecx, ecx
		call	some_invpid
		mov	rcx, [rsp+48h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		add	rsp, 48h
		retn
invpid_wrap	endp

; ---------------------------------------------------------------------------
algn_140002DF2:				; DATA XREF: .pdata:000000014000A27Co
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140002DF4	proc near		; CODE XREF: sub_140003144+126p
					; DATA XREF: .pdata:000000014000A288o

var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
var_18		= qword	ptr -18h

		sub	rsp, 48h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+48h+var_18], rax
		xor	eax, eax
		lea	rdx, [rsp+48h+var_28]
		mov	[rsp+48h+var_28], rax
		mov	word ptr [rsp+48h+var_28], cx
		mov	[rsp+48h+var_20], rax
		lea	ecx, [rax+3]
		call	some_invpid
		mov	rcx, [rsp+48h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		add	rsp, 48h
		retn
sub_140002DF4	endp

; ---------------------------------------------------------------------------
algn_140002E37:				; DATA XREF: .pdata:000000014000A288o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140002E38	proc near		; CODE XREF: sub_140003144:loc_1400031F7p
					; sub_140003144:loc_14000324Ep	...
		xor	al, al
		retn
sub_140002E38	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140002E3C	proc near		; CODE XREF: sub_140003144+C9p
					; sub_140003144+116p ...

var_38		= qword	ptr -38h
var_30		= qword	ptr -30h
var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
var_18		= qword	ptr -18h
arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 50h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+58h+var_18], rax
		mov	rsi, cr3
		mov	cr3, rcx
		xor	edx, edx
		lea	rcx, [rsp+58h+var_38]
		lea	r8d, [rdx+20h]
		call	init_memory
		xor	edi, edi
		lea	rbx, [rsp+58h+var_38]

loc_140002E77:				; CODE XREF: sub_140002E3C+70j
		mov	ecx, edi
		shl	ecx, 0Ch
		add	rcx, cs:page_table_ptr3
		call	cs:__imp_MmGetPhysicalAddress
		xor	rax, [rbx]
		mov	rcx, 1FFFFFFFFFF000h
		and	rax, rcx
		inc	edi
		xor	rax, [rbx]
		or	rax, 1
		mov	[rbx], rax
		lea	rbx, [rbx+8]
		cmp	edi, 4
		jb	short loc_140002E77
		mov	cr3, rsi
		mov	ecx, 280Ah
		vmwrite	rcx, [rsp+58h+var_38]
		mov	ecx, 280Ch
		vmwrite	rcx, [rsp+58h+var_30]
		mov	ecx, 280Eh
		vmwrite	rcx, [rsp+58h+var_28]
		mov	ecx, 2810h
		vmwrite	rcx, [rsp+58h+var_20]
		mov	rcx, [rsp+58h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		mov	rbx, [rsp+58h+arg_0]
		mov	rsi, [rsp+58h+arg_8]
		add	rsp, 50h
		pop	rdi
		retn
sub_140002E3C	endp

; ---------------------------------------------------------------------------
algn_140002EF6:				; DATA XREF: .pdata:000000014000A294o
		align 8

; =============== S U B	R O U T	I N E =======================================

; (target_area,	target_len, pattern, pattern_len

; __int64 __fastcall find_substring_pos(void *Source2)
find_substring_pos proc	near		; CODE XREF: set_func_and_page_table_pointers+99p
					; DATA XREF: .pdata:000000014000A2A0o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r14
		sub	rsp, 20h
		mov	rsi, r9
		mov	r14, r8
		mov	rdi, rdx
		mov	rbp, rcx
		cmp	r9, rdx
		jbe	short loc_140002F26

loc_140002F22:				; CODE XREF: find_substring_pos+56j
		xor	eax, eax
		jmp	short loc_140002F53
; ---------------------------------------------------------------------------

loc_140002F26:				; CODE XREF: find_substring_pos+28j
		sub	rdi, rsi
		mov	rbx, rbp

loc_140002F2C:				; CODE XREF: find_substring_pos+54j
		mov	r8, rsi		; Length
		mov	rdx, rbx	; Source2
		mov	rcx, r14	; Source1
		call	cs:RtlCompareMemory
		cmp	rax, rsi
		jz	short loc_140002F50
		inc	rbx
		mov	rax, rbx
		sub	rax, rbp
		cmp	rax, rdi
		jbe	short loc_140002F2C
		jmp	short loc_140002F22
; ---------------------------------------------------------------------------

loc_140002F50:				; CODE XREF: find_substring_pos+46j
		mov	rax, rbx

loc_140002F53:				; CODE XREF: find_substring_pos+2Cj
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		mov	rdi, [rsp+28h+arg_18]
		add	rsp, 20h
		pop	r14
		retn
find_substring_pos endp

; ---------------------------------------------------------------------------
algn_140002F6E:				; DATA XREF: .pdata:000000014000A2A0o
		align 10h

; =============== S U B	R O U T	I N E =======================================

; Attributes: thunk

MmGetPhysicalAddress proc near		; CODE XREF: sub_140002870+78p
					; sub_140002870+C8p ...
		jmp	cs:__imp_MmGetPhysicalAddress
MmGetPhysicalAddress endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140002F78	proc near		; CODE XREF: sub_140002C58+32p
					; init_CSTRUCT_0x20+D2p
		shr	rcx, 0Ch
		mov	rax, rcx
		retn
sub_140002F78	endp


; =============== S U B	R O U T	I N E =======================================


read_some_msr	proc near		; CODE XREF: sub_140003144+D8p
					; sub_140003144+E5p ...
		rdmsr
		shl	rdx, 20h
		or	rax, rdx
		retn
read_some_msr	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140002F8C	proc near		; CODE XREF: sub_140002870+9Ap
					; sub_1400029E4+37p ...
		shl	rcx, 0Ch
		jmp	cs:MmGetVirtualForPhysical
sub_140002F8C	endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


vm_call_wrapper	proc near		; CODE XREF: sub_14000C638+14p
					; main_run_stuff+BAp
					; DATA XREF: ...
		sub	rsp, 28h

loc_140002F9C:				; DATA XREF: .rdata:00000001400067BCo
		mov	ecx, ecx
		call	do_vmcall
		neg	al
		sbb	eax, eax
		and	eax, 0C0000001h
		jmp	short loc_140002FBB
; ---------------------------------------------------------------------------

loc_140002FAE:				; DATA XREF: .rdata:00000001400067BCo
		mov	rcx, cs:KdDebuggerNotPresent
		cmp	byte ptr [rcx],	0
		jnz	short loc_140002FBB
		int	3		; Trap to Debugger

loc_140002FBB:				; CODE XREF: vm_call_wrapper+14j
					; vm_call_wrapper+20j
		add	rsp, 28h
		retn
vm_call_wrapper	endp


; =============== S U B	R O U T	I N E =======================================


do_vm_read	proc near		; CODE XREF: sub_1400023AC+12p
					; sub_1400026C4+23p ...

arg_8		= qword	ptr  10h

		and	[rsp+arg_8], 0
		mov	eax, ecx
		vmread	rax, rax
		retn
do_vm_read	endp


; =============== S U B	R O U T	I N E =======================================


do_vm_write	proc near		; CODE XREF: sub_1400016D4+11j
					; sub_1400016EC+50j ...
		vmwrite	rcx, rdx
		setz	al
		setb	cl
		adc	al, cl
		retn
do_vm_write	endp


; =============== S U B	R O U T	I N E =======================================


sub_140002FD8	proc near		; CODE XREF: wmsr_stuff+2Cp
		mov	rax, rdx
		shr	rdx, 20h
		wrmsr
		retn
sub_140002FD8	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140002FE4	proc near		; DATA XREF: set_func_and_page_table_pointers+195o
		mov	rax, cs:MmSystemRangeStart
		mov	r10, rdx
		mov	r9, rcx
		cmp	rcx, [rax]
		jb	short loc_140003026
		mov	rdx, cs:qword_140008C38
		mov	rcx, [rdx]

loc_140003000:				; CODE XREF: sub_140002FE4+38j
		cmp	rcx, rdx
		jz	short loc_140003026
		mov	r8, [rcx+30h]
		cmp	r8, r9
		ja	short loc_140003019
		mov	eax, [rcx+40h]
		add	rax, r8
		cmp	r9, rax
		jbe	short loc_14000301E

loc_140003019:				; CODE XREF: sub_140002FE4+28j
		mov	rcx, [rcx]
		jmp	short loc_140003000
; ---------------------------------------------------------------------------

loc_14000301E:				; CODE XREF: sub_140002FE4+33j
		mov	[r10], r8
		mov	rax, [rcx+30h]
		retn
; ---------------------------------------------------------------------------

loc_140003026:				; CODE XREF: sub_140002FE4+10j
					; sub_140002FE4+1Fj
		xor	eax, eax
		retn
sub_140002FE4	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


VM_ENTRY_HANDLER proc near		; CODE XREF: ENTRY_FUNC+41p
					; DATA XREF: .pdata:000000014000A2B8o

var_38		= qword	ptr -38h
var_30		= qword	ptr -30h
var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
var_18		= byte ptr -18h
var_17		= byte ptr -17h
arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 50h
		mov	rdi, cr8
		mov	rbx, cr8
		mov	[rsp+58h+var_38], rcx
		mov	ecx, 6820h
		call	do_vm_read
		mov	ecx, 681Eh
		mov	[rsp+58h+var_30], rax
		call	do_vm_read
		mov	ecx, 681Ch
		mov	[rsp+58h+var_28], rax
		mov	[rsp+58h+var_20], rbx
		mov	[rsp+58h+var_18], dil
		mov	[rsp+58h+var_17], 1
		call	do_vm_read
		mov	rcx, [rsp+58h+var_38]
		mov	[rcx+58h], rax	; guest_rsp
		lea	rcx, [rsp+58h+var_38]
		call	real_handler
		cmp	[rsp+58h+var_17], 0
		jnz	short loc_14000309E
		call	sub_140002D30	; tlb stuff
		call	sub_140002D70

loc_14000309E:				; CODE XREF: VM_ENTRY_HANDLER+66j
		mov	rax, [rsp+58h+var_20]
		mov	cr8, rax
		mov	al, [rsp+58h+var_17]
		mov	rbx, [rsp+58h+arg_0]
		add	rsp, 50h
		pop	rdi
		retn
VM_ENTRY_HANDLER endp

; ---------------------------------------------------------------------------
algn_1400030B6:				; DATA XREF: .pdata:000000014000A2B8o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_1400030B8	proc near		; CODE XREF: ENTRY_FUNC+D9p
					; DATA XREF: .pdata:000000014000A2C4o
		push	rbx
		sub	rsp, 20h
		mov	rbx, rcx
		mov	ecx, 681Eh
		call	do_vm_read
		test	byte ptr [rbx+80h], 40h
		jz	short loc_1400030DE
		mov	ecx, 4400h
		call	do_vm_read

loc_1400030DE:				; CODE XREF: sub_1400030B8+1Aj
		add	rsp, 20h
		pop	rbx
		retn
sub_1400030B8	endp


; =============== S U B	R O U T	I N E =======================================


sub_1400030E4	proc near		; CODE XREF: sub_140003144+1A9j
					; sub_1400032F4+ADj ...

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, rcx
		mov	ecx, 440Ch	; vm_exit_ins_len
		call	do_vm_read
		mov	rdx, [rbx+10h]
		mov	ecx, 681Eh	; guest_rip
		add	rdx, rax
		mov	rdi, rax
		call	do_vm_write
		mov	ecx, [rbx+8]
		bt	rcx, 8
		jnb	short loc_140003138
		xor	r9d, r9d
		xor	r8d, r8d
		lea	edx, [r9+1]
		lea	ecx, [rdx+2]
		call	set_intr_data
		mov	rdx, rdi
		mov	ecx, 401Ah
		call	do_vm_write

loc_140003138:				; CODE XREF: sub_1400030E4+33j
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
sub_1400030E4	endp

; ---------------------------------------------------------------------------
algn_140003143:				; DATA XREF: .pdata:000000014000A2D0o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140003144	proc near		; CODE XREF: real_handler+14Cp
					; DATA XREF: .pdata:000000014000A2DCo

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 20h
		mov	rsi, rcx
		mov	ecx, 6400h
		call	do_vm_read
		mov	rcx, rax
		mov	rdx, rsi
		shr	rcx, 8
		mov	r9, rax
		and	ecx, 0Fh
		call	sub_140004878
		mov	rdi, rax
		mov	rax, r9
		shr	rax, 4
		and	eax, 3
		jz	short loc_1400031CB
		cmp	eax, 1
		jz	short loc_14000319F
		mov	rax, cs:KdDebuggerNotPresent
		cmp	byte ptr [rax],	0
		jnz	loc_1400032DB
		int	3		; Trap to Debugger
		jmp	loc_1400032DB
; ---------------------------------------------------------------------------

loc_14000319F:				; CODE XREF: sub_140003144+43j
		and	r9d, 0Fh
		cmp	r9, 3
		jz	short loc_1400031B9
		cmp	r9, 8
		jnz	loc_1400032DB
		mov	rax, [rsi+18h]
		jmp	short loc_1400031C3
; ---------------------------------------------------------------------------

loc_1400031B9:				; CODE XREF: sub_140003144+63j
		mov	ecx, 6802h
		call	do_vm_read

loc_1400031C3:				; CODE XREF: sub_140003144+73j
		mov	[rdi], rax
		jmp	loc_1400032DB
; ---------------------------------------------------------------------------

loc_1400031CB:				; CODE XREF: sub_140003144+3Ej
		and	r9d, 0Fh
		jz	loc_140003286
		sub	r9, 3
		jz	short loc_14000324E
		sub	r9, 1
		jz	short loc_1400031F7
		cmp	r9, 4
		jnz	loc_1400032DB
		mov	rax, [rdi]
		mov	[rsi+18h], rax
		jmp	loc_1400032DB
; ---------------------------------------------------------------------------

loc_1400031F7:				; CODE XREF: sub_140003144+9Bj
		call	sub_140002E38
		test	al, al
		jz	short loc_140003212
		mov	ecx, 6802h
		call	do_vm_read
		mov	rcx, rax
		call	sub_140002E3C

loc_140003212:				; CODE XREF: sub_140003144+BAj
		call	sub_140002D70
		mov	ecx, 488h
		call	read_some_msr
		mov	ecx, 489h
		mov	rbx, rax
		call	read_some_msr
		mov	rdi, [rdi]
		mov	ecx, 6804h
		and	rdi, rax
		or	rdi, rbx
		mov	rdx, rdi
		call	do_vm_write
		mov	ecx, 6006h
		jmp	loc_1400032D3
; ---------------------------------------------------------------------------

loc_14000324E:				; CODE XREF: sub_140003144+95j
		call	sub_140002E38
		test	al, al
		jz	short loc_14000325F
		mov	rcx, [rdi]
		call	sub_140002E3C

loc_14000325F:				; CODE XREF: sub_140003144+111j
		xor	ecx, ecx
		call	cs:KeGetCurrentProcessorNumberEx
		lea	ecx, [rax+1]
		call	sub_140002DF4
		mov	rdx, [rdi]
		mov	rax, 7FFFFFFFFFFFFFFFh
		and	rdx, rax
		mov	ecx, 6802h
		jmp	short loc_1400032D6
; ---------------------------------------------------------------------------

loc_140003286:				; CODE XREF: sub_140003144+8Bj
		call	sub_140002E38
		test	al, al
		jz	short loc_1400032A1
		mov	ecx, 6802h
		call	do_vm_read
		mov	rcx, rax
		call	sub_140002E3C

loc_1400032A1:				; CODE XREF: sub_140003144+149j
		mov	ecx, 486h
		call	read_some_msr
		mov	ecx, 487h
		mov	rbx, rax
		call	read_some_msr
		mov	rdi, [rdi]
		mov	ecx, 6800h
		and	rdi, rax
		or	rdi, rbx
		mov	rdx, rdi
		call	do_vm_write
		mov	ecx, 6004h

loc_1400032D3:				; CODE XREF: sub_140003144+105j
		mov	rdx, rdi

loc_1400032D6:				; CODE XREF: sub_140003144+140j
		call	do_vm_write

loc_1400032DB:				; CODE XREF: sub_140003144+4Fj
					; sub_140003144+56j ...
		mov	rcx, rsi
		mov	rbx, [rsp+28h+arg_0]
		mov	rsi, [rsp+28h+arg_8]
		add	rsp, 20h
		pop	rdi
		jmp	sub_1400030E4
sub_140003144	endp

; ---------------------------------------------------------------------------
algn_1400032F2:				; DATA XREF: .pdata:000000014000A2DCo
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_1400032F4	proc near		; CODE XREF: real_handler+13Fp
					; DATA XREF: .pdata:000000014000A2E8o

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rdi, rcx
		mov	ecx, 6400h
		call	do_vm_read
		mov	rcx, rax
		mov	rdx, rdi
		shr	rcx, 8
		mov	r9, rax
		and	ecx, 0Fh
		call	sub_140004878
		mov	rbx, rax
		mov	rax, r9
		shr	rax, 4
		and	eax, 1
		jz	short loc_140003394
		cmp	eax, 1
		jnz	short loc_140003394
		and	r9d, 7
		jz	short loc_14000338E
		sub	r9, 1
		jz	short loc_140003389
		sub	r9, 1
		jz	short loc_140003384
		sub	r9, 1
		jz	short loc_14000337F
		sub	r9, 1
		jz	short loc_14000337A
		sub	r9, 1
		jz	short loc_140003375
		sub	r9, 1
		jz	short loc_140003370
		cmp	r9, 1
		jnz	short loc_140003394
		mov	ecx, 681Ah
		call	do_vm_read
		jmp	short loc_140003391
; ---------------------------------------------------------------------------

loc_140003370:				; CODE XREF: sub_1400032F4+68j
		mov	rax, dr6
		jmp	short loc_140003391
; ---------------------------------------------------------------------------

loc_140003375:				; CODE XREF: sub_1400032F4+62j
		mov	rax, dr5
		jmp	short loc_140003391
; ---------------------------------------------------------------------------

loc_14000337A:				; CODE XREF: sub_1400032F4+5Cj
		mov	rax, dr4
		jmp	short loc_140003391
; ---------------------------------------------------------------------------

loc_14000337F:				; CODE XREF: sub_1400032F4+56j
		mov	rax, dr3
		jmp	short loc_140003391
; ---------------------------------------------------------------------------

loc_140003384:				; CODE XREF: sub_1400032F4+50j
		mov	rax, dr2
		jmp	short loc_140003391
; ---------------------------------------------------------------------------

loc_140003389:				; CODE XREF: sub_1400032F4+4Aj
		mov	rax, dr1
		jmp	short loc_140003391
; ---------------------------------------------------------------------------

loc_14000338E:				; CODE XREF: sub_1400032F4+44j
		mov	rax, dr0

loc_140003391:				; CODE XREF: sub_1400032F4+7Aj
					; sub_1400032F4+7Fj ...
		mov	[rbx], rax

loc_140003394:				; CODE XREF: sub_1400032F4+39j
					; sub_1400032F4+3Ej ...
		mov	rcx, rdi
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		jmp	sub_1400030E4
sub_1400032F4	endp

; ---------------------------------------------------------------------------
algn_1400033A6:				; DATA XREF: .pdata:000000014000A2E8o
		align 8

; =============== S U B	R O U T	I N E =======================================


handle_exit_intr proc near		; CODE XREF: real_handler+F2p
					; DATA XREF: .pdata:000000014000A2F4o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		mov	[rsp+arg_10], rsi
		push	rdi
		sub	rsp, 20h
		mov	rbx, rcx
		mov	ecx, 4404h	; vm_exit_intr_info
		call	do_vm_read
		mov	ebp, eax
		movzx	esi, al
		shr	ebp, 8
		and	ebp, 7
		cmp	ebp, 3
		jnz	short loc_140003440
		cmp	esi, 0Eh
		jnz	short loc_140003411
		mov	ecx, 4406h
		call	do_vm_read	; EXIT_INTR_CODE
		mov	ecx, 6400h
		mov	rbx, rax
		call	do_vm_read	; EXIT_QUAL
		mov	r9d, ebx
		mov	r8b, 1
		mov	edx, esi
		mov	ecx, ebp
		mov	rdi, rax
		call	set_intr_data
		mov	rcx, rdi
		call	sub_140001536
		jmp	short loc_140003466
; ---------------------------------------------------------------------------

loc_140003411:				; CODE XREF: handle_exit_intr+34j
		cmp	esi, 0Dh
		jnz	short loc_140003431
		mov	ecx, 4406h
		call	do_vm_read
		mov	r9d, eax
		mov	r8b, 1
		mov	edx, esi
		mov	ecx, ebp
		call	set_intr_data
		jmp	short loc_140003466
; ---------------------------------------------------------------------------

loc_140003431:				; CODE XREF: handle_exit_intr+6Cj
		cmp	esi, 1
		jnz	short loc_140003466
		mov	rcx, rbx
		call	sub_1400030E4
		jmp	short loc_140003466
; ---------------------------------------------------------------------------

loc_140003440:				; CODE XREF: handle_exit_intr+2Fj
		cmp	ebp, 6
		jnz	short loc_140003466
		cmp	esi, 3
		jnz	short loc_140003466
		xor	r9d, r9d
		xor	r8d, r8d
		mov	edx, esi
		mov	ecx, ebp
		call	set_intr_data
		lea	edx, [rbp-5]
		mov	ecx, 401Ah
		call	do_vm_write

loc_140003466:				; CODE XREF: handle_exit_intr+67j
					; handle_exit_intr+87j	...
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		add	rsp, 20h
		pop	rdi
		retn
handle_exit_intr endp

; ---------------------------------------------------------------------------
algn_14000347B:				; DATA XREF: .pdata:000000014000A2F4o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000347C	proc near		; CODE XREF: real_handler+29Fp
					; DATA XREF: .pdata:000000014000A300o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r14
		sub	rsp, 20h
		mov	rbp, rcx
		mov	ecx, 440Eh
		call	do_vm_read
		mov	ecx, 6400h
		mov	rbx, rax
		call	do_vm_read
		xor	esi, esi
		mov	r14, rax
		bt	ebx, 1Bh
		jb	short loc_1400034CD
		mov	ecx, ebx
		mov	rdx, rbp
		shr	ecx, 17h
		and	ecx, 0Fh
		call	sub_140004878
		mov	rsi, [rax]

loc_1400034CD:				; CODE XREF: sub_14000347C+3Cj
		xor	edi, edi
		bt	ebx, 16h
		jb	short loc_14000350D
		mov	ecx, ebx
		mov	rdx, rbp
		shr	ecx, 12h
		and	ecx, 0Fh
		call	sub_140004878
		mov	ecx, ebx
		mov	rdi, [rax]
		and	ecx, 3
		jz	short loc_14000350D
		sub	ecx, 1
		jz	short loc_14000350A
		sub	ecx, 1
		jz	short loc_140003504
		cmp	ecx, 1
		jnz	short loc_14000350D
		shl	rdi, 3
		jmp	short loc_14000350D
; ---------------------------------------------------------------------------

loc_140003504:				; CODE XREF: sub_14000347C+7Bj
		shl	rdi, 2
		jmp	short loc_14000350D
; ---------------------------------------------------------------------------

loc_14000350A:				; CODE XREF: sub_14000347C+76j
		add	rdi, rdi

loc_14000350D:				; CODE XREF: sub_14000347C+57j
					; sub_14000347C+71j ...
		mov	eax, ebx
		xor	ecx, ecx
		shr	eax, 0Fh
		and	eax, 7
		jz	short loc_140003563
		sub	eax, 1
		jz	short loc_14000355C
		sub	eax, 1
		jz	short loc_140003555
		sub	eax, 1
		jz	short loc_14000354E
		sub	eax, 1
		jz	short loc_140003547
		cmp	eax, 1
		jz	short loc_140003540
		mov	rax, cs:KdDebuggerNotPresent
		cmp	[rax], cl
		jnz	short loc_140003570
		int	3		; Trap to Debugger
		jmp	short loc_140003570
; ---------------------------------------------------------------------------

loc_140003540:				; CODE XREF: sub_14000347C+B4j
		mov	ecx, 6810h
		jmp	short loc_140003568
; ---------------------------------------------------------------------------

loc_140003547:				; CODE XREF: sub_14000347C+AFj
		mov	ecx, 680Eh
		jmp	short loc_140003568
; ---------------------------------------------------------------------------

loc_14000354E:				; CODE XREF: sub_14000347C+AAj
		mov	ecx, 680Ch
		jmp	short loc_140003568
; ---------------------------------------------------------------------------

loc_140003555:				; CODE XREF: sub_14000347C+A5j
		mov	ecx, 680Ah
		jmp	short loc_140003568
; ---------------------------------------------------------------------------

loc_14000355C:				; CODE XREF: sub_14000347C+A0j
		mov	ecx, 6808h
		jmp	short loc_140003568
; ---------------------------------------------------------------------------

loc_140003563:				; CODE XREF: sub_14000347C+9Bj
		mov	ecx, 6806h

loc_140003568:				; CODE XREF: sub_14000347C+C9j
					; sub_14000347C+D0j ...
		call	do_vm_read
		mov	rcx, rax

loc_140003570:				; CODE XREF: sub_14000347C+BFj
					; sub_14000347C+C2j
		add	rdi, rcx
		mov	eax, ebx
		add	rdi, rsi
		and	eax, 380h
		add	rdi, r14
		cmp	eax, 80h
		jnz	short loc_140003589
		mov	edi, edi

loc_140003589:				; CODE XREF: sub_14000347C+109j
		mov	ecx, 6802h
		call	do_vm_read
		mov	rsi, cr3
		mov	cr3, rax
		shr	ebx, 1Ch
		and	ebx, 3
		jz	short loc_1400035F3
		sub	ebx, 1
		jz	short loc_1400035E2
		sub	ebx, 1
		jz	short loc_1400035C5
		cmp	ebx, 1
		jnz	short loc_14000360E
		mov	rdx, [rdi+2]
		mov	ecx, 6818h
		call	do_vm_write
		mov	ecx, 4812h
		jmp	short loc_1400035D8
; ---------------------------------------------------------------------------

loc_1400035C5:				; CODE XREF: sub_14000347C+12Dj
		mov	rdx, [rdi+2]
		mov	ecx, 6816h
		call	do_vm_write
		mov	ecx, 4810h

loc_1400035D8:				; CODE XREF: sub_14000347C+147j
		movzx	edx, word ptr [rdi]
		call	do_vm_write
		jmp	short loc_14000360E
; ---------------------------------------------------------------------------

loc_1400035E2:				; CODE XREF: sub_14000347C+128j
		mov	ecx, 6818h
		call	do_vm_read
		mov	ecx, 4812h
		jmp	short loc_140003602
; ---------------------------------------------------------------------------

loc_1400035F3:				; CODE XREF: sub_14000347C+123j
		mov	ecx, 6816h
		call	do_vm_read
		mov	ecx, 4810h

loc_140003602:				; CODE XREF: sub_14000347C+175j
		mov	[rdi+2], rax
		call	do_vm_read
		mov	[rdi], ax

loc_14000360E:				; CODE XREF: sub_14000347C+132j
					; sub_14000347C+164j
		mov	cr3, rsi
		mov	rcx, rbp
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		mov	rdi, [rsp+28h+arg_18]
		add	rsp, 20h
		pop	r14
		jmp	sub_1400030E4
sub_14000347C	endp

; ---------------------------------------------------------------------------
algn_140003633:				; DATA XREF: .pdata:000000014000A300o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_140003634	proc near		; CODE XREF: real_handler+295p
					; DATA XREF: .pdata:000000014000A30Co

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r14
		sub	rsp, 20h
		mov	rbp, rcx
		mov	ecx, 440Eh
		call	do_vm_read
		mov	ecx, 6400h
		mov	rbx, rax
		call	do_vm_read
		mov	r14, rax
		bt	ebx, 0Ah
		jnb	short loc_140003688
		mov	ecx, ebx
		mov	rdx, rbp
		shr	ecx, 3
		and	ecx, 0Fh
		call	sub_140004878
		mov	rdi, rax
		jmp	loc_14000375F
; ---------------------------------------------------------------------------

loc_140003688:				; CODE XREF: sub_140003634+3Aj
		xor	esi, esi
		bt	ebx, 1Bh
		jb	short loc_1400036A3
		mov	ecx, ebx
		mov	rdx, rbp
		shr	ecx, 17h
		and	ecx, 0Fh
		call	sub_140004878
		mov	rsi, [rax]

loc_1400036A3:				; CODE XREF: sub_140003634+5Aj
		xor	edi, edi
		bt	ebx, 16h
		jb	short loc_1400036E3
		mov	ecx, ebx
		mov	rdx, rbp
		shr	ecx, 12h
		and	ecx, 0Fh
		call	sub_140004878
		mov	ecx, ebx
		mov	rdi, [rax]
		and	ecx, 3
		jz	short loc_1400036E3
		sub	ecx, 1
		jz	short loc_1400036E0
		sub	ecx, 1
		jz	short loc_1400036DA
		cmp	ecx, 1
		jnz	short loc_1400036E3
		shl	rdi, 3
		jmp	short loc_1400036E3
; ---------------------------------------------------------------------------

loc_1400036DA:				; CODE XREF: sub_140003634+99j
		shl	rdi, 2
		jmp	short loc_1400036E3
; ---------------------------------------------------------------------------

loc_1400036E0:				; CODE XREF: sub_140003634+94j
		add	rdi, rdi

loc_1400036E3:				; CODE XREF: sub_140003634+75j
					; sub_140003634+8Fj ...
		mov	eax, ebx
		xor	ecx, ecx
		shr	eax, 0Fh
		and	eax, 7
		jz	short loc_140003739
		sub	eax, 1
		jz	short loc_140003732
		sub	eax, 1
		jz	short loc_14000372B
		sub	eax, 1
		jz	short loc_140003724
		sub	eax, 1
		jz	short loc_14000371D
		cmp	eax, 1
		jz	short loc_140003716
		mov	rax, cs:KdDebuggerNotPresent
		cmp	[rax], cl
		jnz	short loc_140003746
		int	3		; Trap to Debugger
		jmp	short loc_140003746
; ---------------------------------------------------------------------------

loc_140003716:				; CODE XREF: sub_140003634+D2j
		mov	ecx, 6810h
		jmp	short loc_14000373E
; ---------------------------------------------------------------------------

loc_14000371D:				; CODE XREF: sub_140003634+CDj
		mov	ecx, 680Eh
		jmp	short loc_14000373E
; ---------------------------------------------------------------------------

loc_140003724:				; CODE XREF: sub_140003634+C8j
		mov	ecx, 680Ch
		jmp	short loc_14000373E
; ---------------------------------------------------------------------------

loc_14000372B:				; CODE XREF: sub_140003634+C3j
		mov	ecx, 680Ah
		jmp	short loc_14000373E
; ---------------------------------------------------------------------------

loc_140003732:				; CODE XREF: sub_140003634+BEj
		mov	ecx, 6808h
		jmp	short loc_14000373E
; ---------------------------------------------------------------------------

loc_140003739:				; CODE XREF: sub_140003634+B9j
		mov	ecx, 6806h

loc_14000373E:				; CODE XREF: sub_140003634+E7j
					; sub_140003634+EEj ...
		call	do_vm_read
		mov	rcx, rax

loc_140003746:				; CODE XREF: sub_140003634+DDj
					; sub_140003634+E0j
		add	rdi, rcx
		mov	eax, ebx
		add	rdi, rsi
		and	eax, 380h
		add	rdi, r14
		cmp	eax, 80h
		jnz	short loc_14000375F
		mov	edi, edi

loc_14000375F:				; CODE XREF: sub_140003634+4Fj
					; sub_140003634+127j
		mov	ecx, 6802h
		call	do_vm_read
		mov	rsi, cr3
		mov	cr3, rax
		shr	ebx, 1Ch
		and	ebx, 3
		jz	short loc_1400037CC
		sub	ebx, 1
		jz	short loc_1400037C5
		sub	ebx, 1
		jz	short loc_1400037B6
		cmp	ebx, 1
		jnz	short loc_1400037D9
		movzx	edx, word ptr [rdi]
		mov	ecx, 80Eh
		call	do_vm_write
		movzx	ebx, word ptr [rdi]
		mov	ecx, 6816h
		call	do_vm_read
		mov	ecx, ebx
		mov	rdx, 20000000000h
		shr	rcx, 3
		or	[rax+rcx*8], rdx
		jmp	short loc_1400037D9
; ---------------------------------------------------------------------------

loc_1400037B6:				; CODE XREF: sub_140003634+14Bj
		movzx	edx, word ptr [rdi]
		mov	ecx, 80Ch
		call	do_vm_write
		jmp	short loc_1400037D9
; ---------------------------------------------------------------------------

loc_1400037C5:				; CODE XREF: sub_140003634+146j
		mov	ecx, 80Eh
		jmp	short loc_1400037D1
; ---------------------------------------------------------------------------

loc_1400037CC:				; CODE XREF: sub_140003634+141j
		mov	ecx, 80Ch

loc_1400037D1:				; CODE XREF: sub_140003634+196j
		call	do_vm_read
		mov	[rdi], ax

loc_1400037D9:				; CODE XREF: sub_140003634+150j
					; sub_140003634+180j ...
		mov	cr3, rsi
		mov	rcx, rbp
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		mov	rdi, [rsp+28h+arg_18]
		add	rsp, 20h
		pop	r14
		jmp	sub_1400030E4
sub_140003634	endp

; ---------------------------------------------------------------------------
algn_1400037FE:				; DATA XREF: .pdata:000000014000A30Co
		align 20h
; [00000003 BYTES: COLLAPSED FUNCTION nullsub_1. PRESS CTRL-NUMPAD+ TO EXPAND]
		align 4

; =============== S U B	R O U T	I N E =======================================


vmread_exit_qual proc near		; CODE XREF: real_handler+2BBp
		mov	ecx, 6400h
		jmp	do_vm_read
vmread_exit_qual endp

; ---------------------------------------------------------------------------
		align 10h

; =============== S U B	R O U T	I N E =======================================

; rdx=0x12
; rcx=ptr to host rsp

VMCALL_HANDLER	proc near		; CODE XREF: real_handler+17Bp
					; DATA XREF: .pdata:000000014000A318o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		mov	[rsp+arg_10], rsi
		push	rdi
		push	r14
		push	r15
		sub	rsp, 20h
		mov	rax, [rcx]
		mov	rsi, rcx
		mov	ecx, 6802h
		mov	ebx, [rax+70h]
		mov	rdi, [rax+68h]
		mov	r15d, [rax+38h]
		call	do_vm_read	; GUEST_CR3
		mov	r14, rax
		mov	rbp, cr3
		mov	eax, 13687453h
		cmp	ebx, eax
		jg	loc_1400042D6
		jz	loc_140004284	; 13687453
		sub	ebx, 13687060h
		jz	loc_1400040BF	; 13687060
					; check0, vmcall0
		sub	ebx, 1
		jz	loc_140003E5E	; check1
		sub	ebx, 1
		jz	loc_140003C26	; check2
		sub	ebx, 1
		jz	short loc_1400038D3 ; check3
		cmp	ebx, 3EEh
		jnz	loc_1400042FE
		mov	rax, [rsi]	; '0x1368744e, check0, vmcall1
		mov	rbx, [rax+88h]
		mov	cr3, r14
		mov	edx, 1000h
		mov	rcx, rdi
		call	allocate_stuff
		mov	rcx, rdi
		call	MmGetPhysicalAddress
		mov	rcx, [rbx+20h]
		mov	rdx, rax
		call	compute_stuff1
		and	qword ptr [rax], 0FFFFFFFFFFFFFFF8h

loc_1400038BE:				; CODE XREF: VMCALL_HANDLER+A6Fj
					; VMCALL_HANDLER+AC1j ...
		mov	rcx, rsi
		call	set_rflags

loc_1400038C6:				; CODE XREF: VMCALL_HANDLER+BBEj
		mov	cr3, rbp

loc_1400038C9:				; CODE XREF: VMCALL_HANDLER+B54j
					; VMCALL_HANDLER+B7Bj ...
		call	sub_140002D30
		jmp	loc_140004321
; ---------------------------------------------------------------------------

loc_1400038D3:				; CODE XREF: VMCALL_HANDLER+6Dj
		mov	cr3, r14	; check3
		mov	dword ptr [rdi], 0E2EA122Ah
		mov	dword ptr [rdi+4], 1721E2E2h
		mov	dword ptr [rdi+8], 0E2E2E2FAh
		mov	dword ptr [rdi+0Ch], 0E2E2E22Bh
		mov	dword ptr [rdi+10h], 0E2E2E3E2h
		mov	dword ptr [rdi+14h], 0E2E2E2E2h
		mov	dword ptr [rdi+18h], 0E2EA2BE2h
		mov	dword ptr [rdi+1Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+20h], 0E2E2E2E2h
		mov	dword ptr [rdi+24h], 0E62BE2E2h
		mov	dword ptr [rdi+28h], 0E2E2E2E2h
		mov	dword ptr [rdi+2Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+30h], 0F8E2E2E2h
		mov	dword ptr [rdi+34h], 0E2E2C20Ch
		mov	dword ptr [rdi+38h], 0C07FDE2h
		mov	dword ptr [rdi+3Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+40h], 0E2EA0AFBh
		mov	dword ptr [rdi+44h], 730E2E2h
		mov	dword ptr [rdi+48h], 0C20CF80Ah
		mov	dword ptr [rdi+4Ch], 0FDE2E2E2h
		mov	dword ptr [rdi+50h], 0E2E30C07h
		mov	dword ptr [rdi+54h], 730E2E2h
		mov	dword ptr [rdi+58h], 0C20CF80Ah
		mov	dword ptr [rdi+5Ch], 0FDE2E2E2h
		mov	dword ptr [rdi+60h], 0E2E00C07h
		mov	dword ptr [rdi+64h], 730E2E2h
		mov	dword ptr [rdi+68h], 0C20CF80Ah
		mov	dword ptr [rdi+6Ch], 0FDE2E2E2h
		mov	dword ptr [rdi+70h], 0E2E10C07h
		mov	dword ptr [rdi+74h], 730E2E2h
		mov	dword ptr [rdi+78h], 0C20CF80Ah
		mov	dword ptr [rdi+7Ch], 0FDE2E2E2h
		mov	dword ptr [rdi+80h], 0E2E60C05h
		mov	dword ptr [rdi+84h], 0AE0E2E2h
		mov	dword ptr [rdi+88h], 7053007h
		mov	dword ptr [rdi+8Ch], 0E2EA073Ah
		mov	dword ptr [rdi+90h], 0E22BE2E2h
		mov	dword ptr [rdi+94h], 0E3E2E2E2h
		mov	dword ptr [rdi+98h], 0E2E2E2E2h
		mov	dword ptr [rdi+9Ch], 0F8E2E2E2h
		mov	dword ptr [rdi+0A0h], 0E2E2C20Ch
		mov	dword ptr [rdi+0A4h], 0C07FDE2h
		mov	dword ptr [rdi+0A8h], 0E2E2E2E2h
		mov	dword ptr [rdi+0ACh], 0E2A407A3h
		mov	dword ptr [rdi+0B0h], 0F2B0E2E2h
		mov	dword ptr [rdi+0B4h], 0E2E22BE2h
		mov	dword ptr [rdi+0B8h], 0E2E2E2E2h
		mov	dword ptr [rdi+0BCh], 0E2E2E2E2h
		mov	dword ptr [rdi+0C0h], 0CF8E2E2h
		mov	dword ptr [rdi+0C4h], 0E2E2E2C2h
		mov	dword ptr [rdi+0C8h], 0E60C07FDh
		mov	dword ptr [rdi+0CCh], 0A3E2E2E2h
		mov	dword ptr [rdi+0D0h], 0E2E2D107h
		mov	dword ptr [rdi+0D4h], 0E2F2B0E2h
		mov	dword ptr [rdi+0D8h], 0E2E2E22Bh
		mov	dword ptr [rdi+0DCh], 0E2E2E2E2h
		mov	dword ptr [rdi+0E0h], 0E2E2E2E2h
		mov	dword ptr [rdi+0E4h], 0E2EAA0E2h
		mov	dword ptr [rdi+0E8h], 0E389E2E2h
		mov	dword ptr [rdi+0ECh], 0F2B0E2E2h
		mov	dword ptr [rdi+0F0h], 0E2E22BE2h
		mov	dword ptr [rdi+0F4h], 0E2E2E2E2h
		mov	dword ptr [rdi+0F8h], 0E2E2E2E2h
		mov	dword ptr [rdi+0FCh], 0CF8E2E2h
		mov	dword ptr [rdi+100h], 0E2E2E2C2h
		mov	dword ptr [rdi+104h], 0E00C0AFDh
		mov	dword ptr [rdi+108h], 0F8E2E2E2h
		mov	dword ptr [rdi+10Ch], 0E2E2C20Ch
		mov	dword ptr [rdi+110h], 0C05FDE2h
		mov	dword ptr [rdi+114h], 0E2E2E2E1h
		mov	dword ptr [rdi+118h], 30070AE0h
		mov	dword ptr [rdi+11Ch], 7A30705h
		mov	dword ptr [rdi+120h], 0E2E2E264h
		mov	dword ptr [rdi+124h], 2BE2F2B0h
		mov	dword ptr [rdi+128h], 0E2E2E2E2h
		mov	dword ptr [rdi+12Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+130h], 0E2E2E2E2h
		mov	dword ptr [rdi+134h], 0E2C20CF8h
		mov	dword ptr [rdi+138h], 0AFDE2E2h
		mov	dword ptr [rdi+13Ch], 0E2E2E30Ch
		mov	dword ptr [rdi+140h], 0C20CF8E2h
		mov	dword ptr [rdi+144h], 0FDE2E2E2h
		mov	dword ptr [rdi+148h], 0E2E00C05h
		mov	dword ptr [rdi+14Ch], 0AE0E2E2h
		mov	dword ptr [rdi+150h], 7053007h
		mov	dword ptr [rdi+154h], 0E24207A3h
		mov	dword ptr [rdi+158h], 0F2B0E2E2h
		mov	dword ptr [rdi+15Ch], 0E2E22BE2h
		mov	dword ptr [rdi+160h], 0E2E2E2E2h
		mov	dword ptr [rdi+164h], 0E2E2E2E2h
		mov	dword ptr [rdi+168h], 0E2F9E2E2h
		mov	dword ptr [rdi+16Ch], 23E2E2E2h
		mov	dword ptr [rdi+170h], 0E2E2FA17h
		mov	word ptr [rdi+174h], 0E3E2h
		jmp	loc_140004274
; ---------------------------------------------------------------------------

loc_140003C26:				; CODE XREF: VMCALL_HANDLER+64j
		mov	cr3, r14	; check2
		mov	dword ptr [rdi], 0E2EA122Ah
		mov	dword ptr [rdi+4], 1721E2E2h
		mov	dword ptr [rdi+8], 0E2E2E2CAh
		mov	dword ptr [rdi+0Ch], 0E2E2E22Bh
		mov	dword ptr [rdi+10h], 0E2E2E3E2h
		mov	dword ptr [rdi+14h], 0E2E2E2E2h
		mov	dword ptr [rdi+18h], 0E2E32BE2h
		mov	dword ptr [rdi+1Ch], 0E262E2E2h
		mov	dword ptr [rdi+20h], 0E2E2E2E2h
		mov	dword ptr [rdi+24h], 0E62BE2E2h
		mov	dword ptr [rdi+28h], 47E2E2E2h
		mov	dword ptr [rdi+2Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+30h], 2BE2E2E2h
		mov	dword ptr [rdi+34h], 0E2E2E2E7h
		mov	dword ptr [rdi+38h], 0E2E2E253h
		mov	dword ptr [rdi+3Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+40h], 0E2E2E42Bh
		mov	dword ptr [rdi+44h], 0E2E2E0E2h
		mov	dword ptr [rdi+48h], 0E2E2E2E2h
		mov	dword ptr [rdi+4Ch], 0E2E52BE2h
		mov	dword ptr [rdi+50h], 0E2AEE2E2h
		mov	dword ptr [rdi+54h], 0E2E2E2E2h
		mov	dword ptr [rdi+58h], 0EA2BE2E2h
		mov	dword ptr [rdi+5Ch], 27E2E2E2h
		mov	dword ptr [rdi+60h], 0E2E2E2E2h
		mov	dword ptr [rdi+64h], 2BE2E2E2h
		mov	dword ptr [rdi+68h], 0E2E2E2EEh
		mov	dword ptr [rdi+6Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+70h], 0E2E2E2E2h
		mov	dword ptr [rdi+74h], 0FBE2F7B2h
		mov	dword ptr [rdi+78h], 0E2E2EE07h
		mov	dword ptr [rdi+7Ch], 0E30733E2h
		mov	dword ptr [rdi+80h], 3AE2E2E2h
		mov	dword ptr [rdi+84h], 0E2E2EE07h
		mov	dword ptr [rdi+88h], 0E2EEA0E2h
		mov	dword ptr [rdi+8Ch], 0E2E7E2E2h
		mov	dword ptr [rdi+90h], 87B6E2E2h
		mov	dword ptr [rdi+94h], 0EE12FFE2h
		mov	dword ptr [rdi+98h], 0F8E2E2E2h
		mov	dword ptr [rdi+9Ch], 0E2E2D20Ch
		mov	dword ptr [rdi+0A0h], 0C07FDE2h
		mov	dword ptr [rdi+0A4h], 0E2E2E212h
		mov	dword ptr [rdi+0A8h], 0E305FCE2h
		mov	dword ptr [rdi+0ACh], 37E2E2E2h
		mov	dword ptr [rdi+0B0h], 7220507h
		mov	dword ptr [rdi+0B4h], 0E2E2E2B0h
		mov	dword ptr [rdi+0B8h], 0E2E2F2F5h
		mov	dword ptr [rdi+0BCh], 0F205FCE2h
		mov	dword ptr [rdi+0C0h], 0FFE2E2E2h
		mov	dword ptr [rdi+0C4h], 0E2E2EE0Ch
		mov	dword ptr [rdi+0C8h], 0C07FCE2h
		mov	dword ptr [rdi+0CCh], 0E2E2E2E6h
		mov	dword ptr [rdi+0D0h], 0B00705A2h
		mov	dword ptr [rdi+0D4h], 0E22BE2F2h
		mov	dword ptr [rdi+0D8h], 0E2E2E2E2h
		mov	dword ptr [rdi+0DCh], 0E2E2E2E2h
		mov	dword ptr [rdi+0E0h], 0FCE2E2E2h
		mov	dword ptr [rdi+0E4h], 0E2E2E307h
		mov	dword ptr [rdi+0E8h], 0B00733E2h
		mov	dword ptr [rdi+0ECh], 0F5E2E2E2h
		mov	dword ptr [rdi+0F0h], 0E2E2E2E3h
		mov	dword ptr [rdi+0F4h], 0F91D61B2h
		mov	dword ptr [rdi+0F8h], 0E2E2E2E2h
		mov	dword ptr [rdi+0FCh], 0E2CA1723h
		mov	word ptr [rdi+100h], 0E2E2h
		mov	byte ptr [rdi+102h], 0E3h
		jmp	loc_140004274
; ---------------------------------------------------------------------------

loc_140003E5E:				; CODE XREF: VMCALL_HANDLER+5Bj
		mov	cr3, r14	; check1
		mov	dword ptr [rdi], 0E2EA122Ah
		mov	dword ptr [rdi+4], 1721E2E2h
		mov	dword ptr [rdi+8], 0E2E2E2CAh
		mov	dword ptr [rdi+0Ch], 0E2E2E22Bh
		mov	dword ptr [rdi+10h], 0E2E2E3E2h
		mov	dword ptr [rdi+14h], 0E2E2E2E2h
		mov	dword ptr [rdi+18h], 0E2EA2BE2h
		mov	dword ptr [rdi+1Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+20h], 0E2E2E2E2h
		mov	dword ptr [rdi+24h], 0EB2BE2E2h
		mov	dword ptr [rdi+28h], 0E5E2E2E2h
		mov	dword ptr [rdi+2Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+30h], 2BE2E2E2h
		mov	dword ptr [rdi+34h], 0E2E2E2E8h
		mov	dword ptr [rdi+38h], 0E2E2E2C8h
		mov	dword ptr [rdi+3Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+40h], 0E2E2E92Bh
		mov	dword ptr [rdi+44h], 0E2E2E1E2h
		mov	dword ptr [rdi+48h], 0E2E2E2E2h
		mov	dword ptr [rdi+4Ch], 0E2EE2BE2h
		mov	dword ptr [rdi+50h], 0E2A6E2E2h
		mov	dword ptr [rdi+54h], 0E2E2E2E2h
		mov	dword ptr [rdi+58h], 0EF2BE2E2h
		mov	dword ptr [rdi+5Ch], 0E4E2E2E2h
		mov	dword ptr [rdi+60h], 0E2E2E2E2h
		mov	dword ptr [rdi+64h], 2BE2E2E2h
		mov	dword ptr [rdi+68h], 0E2E2E2ECh
		mov	dword ptr [rdi+6Ch], 0E2E2E2A7h
		mov	dword ptr [rdi+70h], 0E2E2E2E2h
		mov	dword ptr [rdi+74h], 0E2E2ED2Bh
		mov	dword ptr [rdi+78h], 0E2E2E5E2h
		mov	dword ptr [rdi+7Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+80h], 0E2F22BE2h
		mov	dword ptr [rdi+84h], 0E2C8E2E2h
		mov	dword ptr [rdi+88h], 0E2E2E2E2h
		mov	dword ptr [rdi+8Ch], 0FA2BE2E2h
		mov	dword ptr [rdi+90h], 97E2E2E2h
		mov	dword ptr [rdi+94h], 0E2E2E2E2h
		mov	dword ptr [rdi+98h], 2BE2E2E2h
		mov	dword ptr [rdi+9Ch], 0E2E2E2FEh
		mov	dword ptr [rdi+0A0h], 0E2E2E2E2h
		mov	dword ptr [rdi+0A4h], 0E2E2E2E2h
		mov	dword ptr [rdi+0A8h], 0FBE2F7B2h
		mov	dword ptr [rdi+0ACh], 0E2E2FE07h
		mov	dword ptr [rdi+0B0h], 0E30733E2h
		mov	dword ptr [rdi+0B4h], 3AE2E2E2h
		mov	dword ptr [rdi+0B8h], 0E2E2FE07h
		mov	dword ptr [rdi+0BCh], 0E2FEA0E2h
		mov	dword ptr [rdi+0C0h], 0E2EBE2E2h
		mov	dword ptr [rdi+0C4h], 0A1B6E2E2h
		mov	dword ptr [rdi+0C8h], 0FE12FFE2h
		mov	dword ptr [rdi+0CCh], 0F8E2E2E2h
		mov	dword ptr [rdi+0D0h], 0E2E2D20Ch
		mov	dword ptr [rdi+0D4h], 0C05FDE2h
		mov	dword ptr [rdi+0D8h], 0E2E2E212h
		mov	dword ptr [rdi+0DCh], 0FA07FEE2h
		mov	dword ptr [rdi+0E0h], 37E2E2E2h
		mov	dword ptr [rdi+0E4h], 0CFF0705h
		mov	dword ptr [rdi+0E8h], 0E2E2E2FEh
		mov	dword ptr [rdi+0ECh], 0EA0C07FCh
		mov	dword ptr [rdi+0F0h], 0A2E2E2E2h
		mov	dword ptr [rdi+0F4h], 0F2B00705h
		mov	dword ptr [rdi+0F8h], 0E2E22BE2h
		mov	dword ptr [rdi+0FCh], 0E2E2E2E2h
		mov	dword ptr [rdi+100h], 0E2E2E2E2h
		mov	dword ptr [rdi+104h], 47B2E2E2h
		mov	dword ptr [rdi+108h], 0E2E2F91Dh
		mov	dword ptr [rdi+10Ch], 1723E2E2h
		mov	dword ptr [rdi+110h], 0E2E2E2CAh
		mov	byte ptr [rdi+114h], 0E3h
		jmp	loc_140004274
; ---------------------------------------------------------------------------

loc_1400040BF:				; CODE XREF: VMCALL_HANDLER+52j
		mov	cr3, r14	; 13687060
					; check0, vmcall0
		mov	dword ptr [rdi], 0E2EA122Ah
		mov	dword ptr [rdi+4], 1721E2E2h
		mov	dword ptr [rdi+8], 0E2E2E2FAh
		mov	dword ptr [rdi+0Ch], 0E2E2E22Bh
		mov	dword ptr [rdi+10h], 0E2E2E3E2h
		mov	dword ptr [rdi+14h], 0E2E2E2E2h
		mov	dword ptr [rdi+18h], 0C20CF8E2h
		mov	dword ptr [rdi+1Ch], 0FDE2E2E2h
		mov	dword ptr [rdi+20h], 0E2E20C07h
		mov	dword ptr [rdi+24h], 7A3E2E2h
		mov	dword ptr [rdi+28h], 0E2E2E2B5h
		mov	dword ptr [rdi+2Ch], 2BE2F2B0h
		mov	dword ptr [rdi+30h], 0E2E2E2E2h
		mov	dword ptr [rdi+34h], 0E2E2E2E2h
		mov	dword ptr [rdi+38h], 0E2E2E2E2h
		mov	dword ptr [rdi+3Ch], 0E2C20CF8h
		mov	dword ptr [rdi+40h], 7FDE2E2h
		mov	dword ptr [rdi+44h], 0E2E2E30Ch
		mov	dword ptr [rdi+48h], 8707A3E2h
		mov	dword ptr [rdi+4Ch], 0B0E2E2E2h
		mov	dword ptr [rdi+50h], 0E22BE2F2h
		mov	dword ptr [rdi+54h], 0E2E2E2E2h
		mov	dword ptr [rdi+58h], 0E2E2E2E2h
		mov	dword ptr [rdi+5Ch], 0F8E2E2E2h
		mov	dword ptr [rdi+60h], 0E2E2C20Ch
		mov	dword ptr [rdi+64h], 0C07FDE2h
		mov	dword ptr [rdi+68h], 0E2E2E2E0h
		mov	dword ptr [rdi+6Ch], 0E2D607A3h
		mov	dword ptr [rdi+70h], 0F2B0E2E2h
		mov	dword ptr [rdi+74h], 0E2E22BE2h
		mov	dword ptr [rdi+78h], 0E2E2E2E2h
		mov	dword ptr [rdi+7Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+80h], 0CF8E2E2h
		mov	dword ptr [rdi+84h], 0E2E2E2C2h
		mov	dword ptr [rdi+88h], 0E10C07FDh
		mov	dword ptr [rdi+8Ch], 0A3E2E2E2h
		mov	dword ptr [rdi+90h], 0E2E29007h
		mov	dword ptr [rdi+94h], 0E2F2B0E2h
		mov	dword ptr [rdi+98h], 0E2E2E22Bh
		mov	dword ptr [rdi+9Ch], 0E2E2E2E2h
		mov	dword ptr [rdi+0A0h], 0E2E2E2E2h
		mov	dword ptr [rdi+0A4h], 0C20CF8E2h
		mov	dword ptr [rdi+0A8h], 0FDE2E2E2h
		mov	dword ptr [rdi+0ACh], 0E2E60C07h
		mov	dword ptr [rdi+0B0h], 7A3E2E2h
		mov	dword ptr [rdi+0B4h], 0E2E2E2BDh
		mov	dword ptr [rdi+0B8h], 2BE2F2B0h
		mov	dword ptr [rdi+0BCh], 0E2E2E2E2h
		mov	dword ptr [rdi+0C0h], 0E2E2E2E2h
		mov	dword ptr [rdi+0C4h], 0E2E2E2E2h
		mov	dword ptr [rdi+0C8h], 0E2E2E2F9h
		mov	dword ptr [rdi+0CCh], 0FA1723E2h
		mov	dword ptr [rdi+0D0h], 0E3E2E2E2h

loc_140004274:				; CODE XREF: VMCALL_HANDLER+411j
					; VMCALL_HANDLER+649j ...
		mov	edx, r15d
		mov	rcx, rdi
		call	xordec
		jmp	loc_1400038BE
; ---------------------------------------------------------------------------

loc_140004284:				; CODE XREF: VMCALL_HANDLER+46j
		mov	rax, [rsi]	; 13687453
		mov	rcx, cs:MemoryDescriptorList ; MemoryDescriptorList
		mov	rbx, [rax+88h]
		test	rcx, rcx
		jz	short loc_1400042A8
		call	cs:MmUnlockPages
		and	cs:MemoryDescriptorList, 0

loc_1400042A8:				; CODE XREF: VMCALL_HANDLER+A88j
		mov	cr3, r14
		mov	r8, r15
		xor	edx, edx
		mov	rcx, rdi
		call	init_memory
		mov	rcx, rdi
		call	MmGetPhysicalAddress
		mov	rcx, [rbx+20h]
		mov	rdx, rax
		call	compute_stuff1
		or	qword ptr [rax], 6
		jmp	loc_1400038BE
; ---------------------------------------------------------------------------

loc_1400042D6:				; CODE XREF: VMCALL_HANDLER+40j
		sub	ebx, 13687455h
		jz	loc_140004413
		sub	ebx, 1
		jz	loc_1400043D3
		sub	ebx, 1
		jz	loc_140004390
		sub	ebx, 1
		jz	short loc_140004369
		cmp	ebx, 1
		jz	short loc_14000433A

loc_1400042FE:				; CODE XREF: VMCALL_HANDLER+75j
		mov	ebx, 3

loc_140004303:				; CODE XREF: VMCALL_HANDLER+C17j
		xor	r9d, r9d
		xor	r8d, r8d
		mov	ecx, ebx
		lea	edx, [r9+6]
		call	set_intr_data
		mov	rdx, rbx
		mov	ecx, 401Ah	; vmentry_ins_len
		call	do_vm_write

loc_140004321:				; CODE XREF: VMCALL_HANDLER+BEj
					; VMCALL_HANDLER+C28j
		mov	rbx, [rsp+38h+arg_0]
		mov	rbp, [rsp+38h+arg_8]
		mov	rsi, [rsp+38h+arg_10]
		add	rsp, 20h
		pop	r15
		pop	r14
		pop	rdi
		retn
; ---------------------------------------------------------------------------

loc_14000433A:				; CODE XREF: VMCALL_HANDLER+AECj
		mov	rax, [rsi]
		mov	rcx, rdi
		mov	rbx, [rax+88h]
		call	MmGetPhysicalAddress
		mov	rcx, [rbx+20h]
		mov	rdx, rax
		call	compute_stuff1
		and	qword ptr [rax], 0FFFFFFFFFFFFFFFEh

loc_14000435C:				; CODE XREF: VMCALL_HANDLER+BD8j
		mov	rcx, rsi
		call	set_rflags
		jmp	loc_1400038C9
; ---------------------------------------------------------------------------

loc_140004369:				; CODE XREF: VMCALL_HANDLER+AE7j
		mov	rax, [rsi]
		mov	rcx, rdi
		mov	rbx, [rax+88h]
		call	MmGetPhysicalAddress
		mov	rcx, [rbx+20h]
		mov	rdx, rax
		call	compute_stuff1
		and	qword ptr [rax], 0FFFFFFFFFFFFFFFDh
		jmp	loc_1400038C9
; ---------------------------------------------------------------------------

loc_140004390:				; CODE XREF: VMCALL_HANDLER+ADEj
		mov	cr3, r14
		mov	rax, [rsi]
		mov	rdx, rdi
		mov	rcx, [rax+88h]
		call	do_something_to_text_seg
		test	al, al
		jnz	loc_1400038BE
		xor	r9d, r9d
		xor	r8d, r8d
		lea	edx, [r9+6]
		lea	ebx, [rdx-3]
		mov	ecx, ebx
		call	set_intr_data
		mov	edx, ebx
		mov	ecx, 401Ah	; vmentry_ins_len
		call	do_vm_write
		jmp	loc_1400038C6
; ---------------------------------------------------------------------------

loc_1400043D3:				; CODE XREF: VMCALL_HANDLER+AD5j
		mov	rax, [rsi]
		mov	rdx, [rdi+18h]
		mov	rcx, [rax+88h]
		call	do_something_to_text_seg
		test	al, al
		jnz	loc_14000435C
		xor	r9d, r9d
		xor	r8d, r8d
		lea	edx, [r9+6]
		lea	ebx, [rdx-3]
		mov	ecx, ebx
		call	set_intr_data
		mov	edx, ebx
		mov	ecx, 401Ah	; VM_ENTRY_INS_LEN
		call	do_vm_write
		jmp	loc_1400038C9
; ---------------------------------------------------------------------------

loc_140004413:				; CODE XREF: VMCALL_HANDLER+ACCj
		mov	ecx, 4818h
		call	do_vm_read	; GUESS_SS_AR_BYTES
		shr	eax, 5
		mov	ebx, 3
		test	bl, al
		jnz	loc_140004303
		mov	rdx, rdi
		mov	rcx, rsi
		call	sub_140004440
		jmp	loc_140004321
VMCALL_HANDLER	endp

; ---------------------------------------------------------------------------
algn_14000443D:				; DATA XREF: .pdata:000000014000A318o
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140004440	proc near		; CODE XREF: VMCALL_HANDLER+C23p
					; DATA XREF: .pdata:000000014000A324o

var_48		= word ptr -48h
var_46		= qword	ptr -46h
var_38		= byte ptr -38h
var_28		= qword	ptr -28h
var_18		= byte ptr -18h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	[rsp+arg_10], rbx
		mov	[rsp+arg_18], rsi
		push	rdi
		push	r14
		push	r15
		sub	rsp, 50h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+68h+var_28], rax
		mov	r15, rcx
		mov	r14, rdx
		mov	ecx, 4810h
		call	do_vm_read
		mov	ecx, 6816h
		mov	rsi, rax
		call	do_vm_read
		mov	ecx, 4812h
		mov	rdi, rax
		call	do_vm_read
		mov	ecx, 6818h
		mov	rbx, rax
		call	do_vm_read
		lea	rcx, [rsp+68h+var_48]
		mov	[rsp+68h+var_48], si
		mov	[rsp+68h+var_46], rdi
		mov	word ptr [rsp+68h+var_38], bx
		mov	qword ptr [rsp+68h+var_38+2], rax
		call	sub_1400014E4
		lidt	fword ptr [rsp+68h+var_38]
		mov	rax, [r15]
		mov	rcx, [rax+88h]
		mov	[r14], rcx
		mov	ecx, 440Ch
		call	do_vm_read
		and	qword ptr [r15+8], 0FFFFFFFFFFFFF72Ah
		mov	rdx, [r15+10h]
		add	rdx, rax
		mov	rax, [r15]
		mov	[rax+70h], rdx
		mov	rcx, [r15]
		mov	rax, [rcx+58h]
		mov	[rcx+68h], rax
		mov	rcx, [r15]
		mov	rax, [r15+8]
		mov	[rcx+78h], rax
		mov	byte ptr [r15+21h], 0
		mov	rcx, [rsp+68h+var_28]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		lea	r11, [rsp+68h+var_18]
		mov	rbx, [r11+30h]
		mov	rsi, [r11+38h]
		mov	rsp, r11
		pop	r15
		pop	r14
		pop	rdi
		retn
sub_140004440	endp

; ---------------------------------------------------------------------------
algn_140004527:				; DATA XREF: .pdata:000000014000A324o
		align 8

; =============== S U B	R O U T	I N E =======================================


real_handler	proc near		; CODE XREF: VM_ENTRY_HANDLER+5Cp
					; DATA XREF: .pdata:000000014000A330o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 30h
		mov	rdi, rcx
		mov	ecx, 4402h
		call	do_vm_read
		movzx	edx, ax		; exit reason
		cmp	edx, 1Eh
		ja	loc_1400046AD
		jz	loc_1400047CC
		cmp	edx, 10h
		ja	loc_140004646
		jz	loc_140004624	; RDTSC
		test	edx, edx
		jz	loc_140004617	; exception_NMI
		sub	edx, 2
		jz	loc_1400047D7	; triple_fault
		sub	edx, 8
		jz	short loc_1400045B5 ; CPUID
		sub	edx, 3
		jz	short loc_1400045AE ; INVD
		cmp	edx, 1
		jnz	loc_1400047E0	; DO_EXIT
		mov	ecx, 6400h	; INVLPG
		call	do_vm_read
		mov	rbx, rax
		invlpg	byte ptr [rax]
		xor	ecx, ecx
		call	cs:KeGetCurrentProcessorNumberEx
		mov	ecx, 1
		mov	rdx, rbx
		add	cx, ax
		call	invpid_wrap
		jmp	short loc_14000460A
; ---------------------------------------------------------------------------

loc_1400045AE:				; CODE XREF: real_handler+51j
		call	sub_140001533	; INVD
		jmp	short loc_14000460A
; ---------------------------------------------------------------------------

loc_1400045B5:				; CODE XREF: real_handler+4Cj
		mov	r10, [rdi]	; CPUID
		mov	r9d, [r10+78h]
		mov	eax, r9d
		mov	ecx, [r10+70h]
		cpuid
		mov	r8d, ecx
		mov	ecx, 1
		cmp	r9d, ecx
		jnz	short loc_1400045D9
		bts	r8d, 1Fh
		jmp	short loc_1400045E8
; ---------------------------------------------------------------------------

loc_1400045D9:				; CODE XREF: real_handler+A8j
		cmp	r9d, 40000001h
		mov	ecx, 56484C46h
		cmovz	eax, ecx

loc_1400045E8:				; CODE XREF: real_handler+AFj
		mov	eax, eax
		mov	[r10+78h], rax
		mov	rax, [rdi]
		mov	ecx, ebx
		mov	[rax+60h], rcx
		mov	rax, [rdi]
		mov	ecx, r8d
		mov	[rax+70h], rcx
		mov	rax, [rdi]
		mov	ecx, edx
		mov	[rax+68h], rcx

loc_14000460A:				; CODE XREF: real_handler+84j
					; real_handler+8Bj ...
		mov	rcx, rdi
		call	sub_1400030E4
		jmp	loc_1400047CC
; ---------------------------------------------------------------------------

loc_140004617:				; CODE XREF: real_handler+3Aj
		mov	rcx, rdi	; exception_NMI
		call	handle_exit_intr
		jmp	loc_1400047CC
; ---------------------------------------------------------------------------

loc_140004624:				; CODE XREF: real_handler+32j
		rdtsc			; RDTSC
		mov	rcx, [rdi]
		shl	rdx, 20h
		or	rax, rdx
		mov	rdx, rax
		shr	rdx, 20h
		mov	[rcx+68h], rdx
		mov	ecx, eax
		mov	rax, [rdi]
		mov	[rax+78h], rcx
		jmp	short loc_14000460A
; ---------------------------------------------------------------------------

loc_140004646:				; CODE XREF: real_handler+2Cj
		cmp	edx, 12h
		jz	short loc_1400046A0 ; VMCALL
		jbe	loc_1400047E0	; DO_EXIT
		cmp	edx, 1Bh
		jbe	short loc_14000467E ; EXIT_REASON <= VMXON
		cmp	edx, 1Ch
		jz	short loc_140004671
		cmp	edx, 1Dh
		jnz	loc_1400047E0	; DO_EXIT
		mov	rcx, rdi	; DR_ACCESS
		call	sub_1400032F4
		jmp	loc_1400047CC
; ---------------------------------------------------------------------------

loc_140004671:				; CODE XREF: real_handler+131j
		mov	rcx, rdi	; CR_ACCESS
		call	sub_140003144
		jmp	loc_1400047CC
; ---------------------------------------------------------------------------

loc_14000467E:				; CODE XREF: real_handler+12Cj
		mov	rdx, [rdi+8]	; EXIT_REASON <= VMXON
		mov	ecx, 6820h	; ldtr_ar_bytes
		and	rdx, 0FFFFFFFFFFFFF72Bh
		or	rdx, 1
		mov	[rdi+8], rdx
		call	do_vm_write
		jmp	loc_14000460A
; ---------------------------------------------------------------------------

loc_1400046A0:				; CODE XREF: real_handler+121j
		mov	rcx, rdi	; VMCALL
		call	VMCALL_HANDLER	; rdx=0x12
					; rcx=ptr to host rsp
		jmp	loc_1400047CC
; ---------------------------------------------------------------------------

loc_1400046AD:				; CODE XREF: real_handler+1Dj
		sub	edx, 1Fh
		jz	loc_1400047CC
		sub	edx, 1
		jz	loc_1400047CC
		sub	edx, 5
		jz	loc_1400047CC
		sub	edx, 9
		jz	loc_1400047C4	; ACCESS_GDTR_OR_IDTR
		sub	edx, 1
		jz	loc_1400047BA	; ACCESS_LDTR_OR_TR
		sub	edx, 1
		jz	loc_14000476E	; reason=48 = EPT_VIOLATION
		sub	edx, 1
		jz	short loc_140004762 ; EPT_MISSCONFIG
		sub	edx, 2
		jz	short loc_140004725 ; EDT_RDTSCP
		cmp	edx, 4
		jnz	loc_1400047E0	; DO_EXIT
		mov	rcx, [rdi]	; edt_INVVPID
		xor	eax, eax
		mov	[rsp+38h+arg_8], rax
		mov	eax, [rcx+78h]
		mov	dword ptr [rsp+38h+arg_8], eax
		mov	eax, [rcx+68h]
		mov	ecx, [rcx+70h]
		mov	dword ptr [rsp+38h+arg_8+4], eax
		mov	rdx, [rsp+38h+arg_8]
		mov	rax, rdx
		shr	rdx, 20h
		xsetbv
		jmp	loc_14000460A
; ---------------------------------------------------------------------------

loc_140004725:				; CODE XREF: real_handler+1C3j
		and	dword ptr [rsp+38h+arg_8], 0 ; EDT_RDTSCP
		rdtscp
		shl	rdx, 20h
		lea	rbx, [rsp+38h+arg_8]
		or	rax, rdx
		mov	[rbx], ecx
		mov	rcx, [rdi]
		mov	rdx, rax
		shr	rdx, 20h
		mov	[rcx+68h], rdx
		mov	ecx, eax
		mov	rax, [rdi]
		mov	[rax+78h], rcx
		mov	rax, [rdi]
		mov	ecx, dword ptr [rsp+38h+arg_8]
		mov	[rax+70h], rcx
		jmp	loc_14000460A
; ---------------------------------------------------------------------------

loc_140004762:				; CODE XREF: real_handler+1BEj
		mov	ecx, 2400h	; EPT_MISSCONFIG
		call	do_vm_read	; GUEST_PHYSICAL_ADDRESS
		jmp	short loc_1400047CC
; ---------------------------------------------------------------------------

loc_14000476E:				; CODE XREF: real_handler+1B5j
		mov	rax, [rdi]	; reason=48 = EPT_VIOLATION
		mov	rcx, [rax+88h]
		mov	rcx, [rcx+20h]
		call	sub_1400026C4
		mov	ecx, 440Ch
		mov	ebx, eax
		call	do_vm_read
		mov	ecx, 1
		mov	rdx, rax
		cmp	ebx, ecx
		jnz	short loc_1400047A3
		mov	rcx, rdi
		call	sub_1400023AC
		jmp	short loc_1400047CC
; ---------------------------------------------------------------------------

loc_1400047A3:				; CODE XREF: real_handler+26Fj
		lea	eax, [rbx-2]
		cmp	eax, ecx
		ja	short loc_1400047CC
		add	rdx, [rdi+10h]
		mov	ecx, 681Eh
		call	do_vm_write
		jmp	short loc_1400047CC
; ---------------------------------------------------------------------------

loc_1400047BA:				; CODE XREF: real_handler+1ACj
		mov	rcx, rdi	; ACCESS_LDTR_OR_TR
		call	sub_140003634
		jmp	short loc_1400047CC
; ---------------------------------------------------------------------------

loc_1400047C4:				; CODE XREF: real_handler+1A3j
		mov	rcx, rdi	; ACCESS_GDTR_OR_IDTR
		call	sub_14000347C

loc_1400047CC:				; CODE XREF: real_handler+23j
					; real_handler+EAj ...
		mov	rbx, [rsp+38h+arg_0]
		add	rsp, 30h
		pop	rdi
		retn
; ---------------------------------------------------------------------------

loc_1400047D7:				; CODE XREF: real_handler+43j
		mov	rcx, rdi	; triple_fault
		call	nullsub_1
		int	3		; Trap to Debugger
; ---------------------------------------------------------------------------

loc_1400047E0:				; CODE XREF: real_handler+56j
					; real_handler+123j ...
		mov	rcx, rdi	; DO_EXIT
		call	vmread_exit_qual
		retn
real_handler	endp ; sp-analysis failed

; ---------------------------------------------------------------------------
unk_1400047E9	db 0CCh	; Ã		; DATA XREF: .pdata:000000014000A330o
		db 0CCh	; Ã
		db 0CCh	; Ã

; =============== S U B	R O U T	I N E =======================================


set_rflags	proc near		; CODE XREF: VMCALL_HANDLER+B1p
					; VMCALL_HANDLER+B4Fp
					; DATA XREF: ...
		push	rbx
		sub	rsp, 20h
		mov	rdx, [rcx+8]
		mov	rbx, rcx
		and	rdx, 0FFFFFFFFFFFFF72Ah
		mov	[rcx+8], rdx
		mov	ecx, 6820h
		call	do_vm_write
		mov	rcx, rbx
		add	rsp, 20h
		pop	rbx
		jmp	sub_1400030E4
set_rflags	endp

; ---------------------------------------------------------------------------
algn_14000481B:				; DATA XREF: .pdata:000000014000A33Co
		align 4

; =============== S U B	R O U T	I N E =======================================


set_intr_data	proc near		; CODE XREF: sub_1400030E4+42p
					; handle_exit_intr+5Ap	...

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		and	ecx, 7
		movzx	ebx, r8b
		mov	eax, ebx
		movzx	edx, dl
		or	eax, 0FFF00000h
		mov	edi, r9d
		shl	eax, 3
		xor	r10d, r10d
		or	eax, ecx
		and	r10d, 0FFFFF000h
		shl	eax, 8
		mov	ecx, 4016h
		or	eax, r10d
		or	edx, eax
		call	do_vm_write	; vmentry_intr_info
		test	bl, bl
		jz	short loc_14000486B
		mov	edx, edi
		mov	ecx, 4018h	; vmentry_exception_error_code
		call	do_vm_write

loc_14000486B:				; CODE XREF: set_intr_data+41j
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
set_intr_data	endp

; ---------------------------------------------------------------------------
algn_140004876:				; DATA XREF: .pdata:000000014000A348o
		align 8
; Node #0
		jz	loc_14000490F
		test	ecx, ecx
		jz	short loc_140004906
		sub	ecx, 1
		jz	short loc_1400048FD
		sub	ecx, 1
		jz	short loc_1400048F1
		sub	ecx, 1
		jz	short loc_1400048E5
		sub	ecx, 1
		jz	short loc_1400048D9
		sub	ecx, 1
		jz	short loc_1400048CD
		sub	ecx, 1
		jz	short loc_1400048C1
		cmp	ecx, 1
		jnz	loc_14000493B
		mov	r8, [rdx]
		add	r8, 40h
		jmp	loc_140004983
; ---------------------------------------------------------------------------

loc_1400048C1:				; CODE XREF: sub_140004878+32j
		mov	r8, [rdx]
		add	r8, 48h
		jmp	loc_140004983
; ---------------------------------------------------------------------------

loc_1400048CD:				; CODE XREF: sub_140004878+2Dj
		mov	r8, [rdx]
		add	r8, 50h
		jmp	loc_140004983
; ---------------------------------------------------------------------------

loc_1400048D9:				; CODE XREF: sub_140004878+28j
		mov	r8, [rdx]
		add	r8, 58h
		jmp	loc_140004983
; ---------------------------------------------------------------------------

loc_1400048E5:				; CODE XREF: sub_140004878+23j
		mov	r8, [rdx]
		add	r8, 60h
		jmp	loc_140004983
; ---------------------------------------------------------------------------

loc_1400048F1:				; CODE XREF: sub_140004878+1Ej
		mov	r8, [rdx]
		add	r8, 68h
		jmp	loc_140004983
; ---------------------------------------------------------------------------

loc_1400048FD:				; CODE XREF: sub_140004878+19j
		mov	r8, [rdx]
		add	r8, 70h
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_140004906:				; CODE XREF: sub_140004878+14j
		mov	r8, [rdx]
		add	r8, 78h
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_14000490F:				; CODE XREF: sub_140004878+Cj
		mov	r8, [rdx]
		add	r8, 38h
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_140004918:				; CODE XREF: sub_140004878+6j
		sub	ecx, 9
		jz	short loc_14000497C
		sub	ecx, 1
		jz	short loc_140004973
		sub	ecx, 1
		jz	short loc_14000496A
		sub	ecx, 1
		jz	short loc_140004961
		sub	ecx, 1
		jz	short loc_140004958
		sub	ecx, 1
		jz	short loc_14000494F
		cmp	ecx, 1
		jz	short loc_14000494A

loc_14000493B:				; CODE XREF: sub_140004878+37j
		mov	rax, cs:KdDebuggerNotPresent
		cmp	[rax], r8b
		jnz	short loc_140004983
		int	3		; Trap to Debugger
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_14000494A:				; CODE XREF: sub_140004878+C1j
		mov	r8, [rdx]
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_14000494F:				; CODE XREF: sub_140004878+BCj
		mov	r8, [rdx]
		add	r8, 8
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_140004958:				; CODE XREF: sub_140004878+B7j
		mov	r8, [rdx]
		add	r8, 10h
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_140004961:				; CODE XREF: sub_140004878+B2j
		mov	r8, [rdx]
		add	r8, 18h
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_14000496A:				; CODE XREF: sub_140004878+ADj
		mov	r8, [rdx]
		add	r8, 20h
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_140004973:				; CODE XREF: sub_140004878+A8j
		mov	r8, [rdx]
		add	r8, 28h
		jmp	short loc_140004983
; ---------------------------------------------------------------------------

loc_14000497C:				; CODE XREF: sub_140004878+A3j
		mov	r8, [rdx]
		add	r8, 30h

loc_140004983:				; CODE XREF: sub_140004878+44j
					; sub_140004878+50j ...
		mov	rax, r8
		retn
sub_140004878	endp

; ---------------------------------------------------------------------------
		align 8

; =============== S U B	R O U T	I N E =======================================


allocate_stuff	proc near		; CODE XREF: VMCALL_HANDLER+91p
					; DATA XREF: .pdata:000000014000A354o

var_28		= qword	ptr -28h
Priority	= dword	ptr -20h
Mdl		= qword	ptr -18h
arg_0		= qword	ptr  8
arg_10		= dword	ptr  18h

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 40h
		mov	edi, 0C0000001h
		mov	[rsp+48h+arg_10], edi

loc_14000499B:				; DATA XREF: .rdata:0000000140006968o
		and	[rsp+48h+var_28], 0
		mov	r9b, 1		; ChargeQuota
		xor	r8d, r8d	; SecondaryBuffer
		call	cs:IoAllocateMdl
		mov	rbx, rax
		mov	[rsp+48h+Mdl], rax
		test	rax, rax
		jnz	short loc_1400049C1
		mov	edi, 0C000009Ah
		jmp	short loc_140004A2E
; ---------------------------------------------------------------------------

loc_1400049C1:				; CODE XREF: allocate_stuff+30j
					; DATA XREF: .rdata:0000000140006958o
		xor	r8d, r8d	; Operation
		xor	edx, edx	; AccessMode
		mov	rcx, rbx	; MemoryDescriptorList
		call	cs:MmProbeAndLockPages
		nop

loc_1400049D0:				; DATA XREF: .rdata:0000000140006958o
		test	byte ptr [rbx+0Ah], 5
		jz	short loc_1400049DC
		mov	rax, [rbx+18h]
		jmp	short loc_1400049FB
; ---------------------------------------------------------------------------

loc_1400049DC:				; CODE XREF: allocate_stuff+4Cj
		mov	[rsp+48h+Priority], 10h	; Priority
		and	dword ptr [rsp+48h+var_28], 0
		xor	r9d, r9d	; BaseAddress
		xor	edx, edx	; AccessMode
		lea	r8d, [r9+1]	; CacheType
		mov	rcx, rbx	; MemoryDescriptorList
		call	cs:MmMapLockedPagesSpecifyCache

loc_1400049FB:				; CODE XREF: allocate_stuff+52j
		test	rax, rax
		jnz	short loc_140004A14
		mov	rcx, rbx	; MemoryDescriptorList
		call	cs:MmUnlockPages
		mov	rcx, rbx	; Mdl
		call	cs:IoFreeMdl
		jmp	short loc_140004A2E
; ---------------------------------------------------------------------------

loc_140004A14:				; CODE XREF: allocate_stuff+76j
		mov	cs:MemoryDescriptorList, rbx
		xor	edi, edi
		jmp	short loc_140004A2E
; ---------------------------------------------------------------------------

loc_140004A1F:				; DATA XREF: .rdata:0000000140006958o
		mov	rcx, [rsp+48h+Mdl] ; Mdl
		call	cs:IoFreeMdl
		mov	edi, [rsp+48h+arg_10]

loc_140004A2E:				; CODE XREF: allocate_stuff+37j
					; allocate_stuff+8Aj ...
		mov	eax, edi
		mov	rbx, [rsp+48h+arg_0]
		add	rsp, 40h
		pop	rdi
		retn
allocate_stuff	endp

; ---------------------------------------------------------------------------
algn_140004A3B:				; DATA XREF: .pdata:000000014000A354o
		align 4

; =============== S U B	R O U T	I N E =======================================


do_something_to_text_seg proc near	; CODE XREF: VMCALL_HANDLER+B91p
					; VMCALL_HANDLER+BD1p
					; DATA XREF: ...

var_38		= dword	ptr -38h
var_30		= qword	ptr -30h
arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		push	r12
		push	r13
		push	r14
		push	r15
		sub	rsp, 30h
		mov	r14, rdx
		mov	r13, rcx
		xor	ebx, ebx
		mov	r12d, ebx

loc_140004A5E:				; DATA XREF: .rdata:00000001400069A8o
		movsxd	rsi, dword ptr [rdx+3Ch]
		movzx	eax, word ptr [rsi+rdx+14h]
		add	rdx, 18h
		add	rdx, rsi
		add	rdx, rax
		mov	[rsp+58h+arg_10], rdx
		mov	edi, ebx
		mov	[rsp+58h+var_38], ebx

loc_140004A7C:				; CODE XREF: do_something_to_text_seg+7Fj
		movzx	eax, word ptr [rsi+r14+6]
		cmp	edi, eax
		jnb	short loc_140004ABD
		mov	eax, edi
		lea	rcx, [rax+rax*4]
		lea	r15, [rdx+rcx*8]
		lea	rdx, Str2	; ".text"
		mov	rcx, r15	; Str1
		call	strcmp
		test	eax, eax
		jnz	short loc_140004AB0
		mov	r12d, [r15+10h]
		mov	edi, [r15+0Ch]
		add	rdi, r14
		jmp	short loc_140004AC0
; ---------------------------------------------------------------------------

loc_140004AB0:				; CODE XREF: do_something_to_text_seg+65j
		inc	edi
		mov	[rsp+58h+var_38], edi
		mov	rdx, [rsp+58h+arg_10]
		jmp	short loc_140004A7C
; ---------------------------------------------------------------------------

loc_140004ABD:				; CODE XREF: do_something_to_text_seg+48j
		mov	rdi, rbx

loc_140004AC0:				; CODE XREF: do_something_to_text_seg+72j
		test	rdi, rdi
		jz	short loc_140004AFB
		mov	rbx, rdi

loc_140004AC8:				; CODE XREF: do_something_to_text_seg+BBj
		mov	[rsp+58h+var_30], rbx
		mov	eax, r12d
		add	rax, rdi
		cmp	rbx, rax
		jnb	short loc_140004AF9
		mov	rcx, rbx
		call	MmGetPhysicalAddress
		mov	rdx, rax
		mov	rcx, [r13+20h]
		call	compute_stuff1
		and	qword ptr [rax], 0FFFFFFFFFFFFFFFDh
		add	rbx, 1000h
		jmp	short loc_140004AC8
; ---------------------------------------------------------------------------

loc_140004AF9:				; CODE XREF: do_something_to_text_seg+9Aj
		mov	bl, 1

loc_140004AFB:				; CODE XREF: do_something_to_text_seg+87j
					; DATA XREF: .rdata:00000001400069A8o
		mov	al, bl
		mov	rbx, [rsp+58h+arg_0]
		mov	rsi, [rsp+58h+arg_8]
		add	rsp, 30h
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	rdi
		retn
do_something_to_text_seg endp

; ---------------------------------------------------------------------------
algn_140004B15:				; DATA XREF: .pdata:000000014000A360o
		align 8

; =============== S U B	R O U T	I N E =======================================


xordec		proc near		; CODE XREF: VMCALL_HANDLER+A6Ap
		mov	cs:do_some_xor_decode, 6B05B5E2h
		test	edx, edx
		jz	short locret_140004B34
		mov	eax, edx

loc_140004B28:				; CODE XREF: xordec+1Aj
		xor	byte ptr [rcx],	0E2h
		inc	rcx
		sub	rax, 1
		jnz	short loc_140004B28

locret_140004B34:			; CODE XREF: xordec+Cj
		retn
xordec		endp

; ---------------------------------------------------------------------------
		db 11h dup(0CCh)
		align 10h

; =============== S U B	R O U T	I N E =======================================


; __int64 __fastcall sub_140004B50(ULONG_PTR BugCheckParameter1)
sub_140004B50	proc near		; CODE XREF: sub_140002D30+34p
					; sub_140002D70+34p ...

var_18		= qword	ptr -18h

		cmp	rcx, cs:__security_cookie
		jnz	short loc_140004B69
		rol	rcx, 10h
		test	cx, 0FFFFh
		jnz	short loc_140004B65
		retn
; ---------------------------------------------------------------------------

loc_140004B65:				; CODE XREF: sub_140004B50+12j
		ror	rcx, 10h

loc_140004B69:				; CODE XREF: sub_140004B50+7j
		jmp	loc_140004B70
; ---------------------------------------------------------------------------
algn_140004B6E:				; DATA XREF: .pdata:000000014000A36Co
		align 10h

loc_140004B70:				; CODE XREF: sub_140004B50:loc_140004B69j
					; DATA XREF: .pdata:000000014000A378o
		sub	rsp, 38h
		and	[rsp+38h+var_18], 0
		mov	rdx, rcx	; BugCheckParameter1
		mov	r9, cs:BugCheckParameter3 ; BugCheckParameter3
		mov	ecx, 0F7h	; BugCheckCode
		mov	r8, cs:__security_cookie ; BugCheckParameter2
		call	cs:KeBugCheckEx
sub_140004B50	endp

; ---------------------------------------------------------------------------
algn_140004B96:				; DATA XREF: .pdata:000000014000A378o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140004B98	proc near		; DATA XREF: .rdata:0000000140006634o
					; .rdata:0000000140006654o ...
		sub	rsp, 28h
		mov	r8, [r9+38h]
		mov	rcx, rdx
		mov	rdx, r9
		call	sub_140004BB8
		mov	eax, 1
		add	rsp, 28h
		retn
sub_140004B98	endp

; ---------------------------------------------------------------------------
algn_140004BB5:				; DATA XREF: .pdata:000000014000A384o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_140004BB8	proc near		; CODE XREF: sub_140004B98+Ep
					; DATA XREF: .pdata:000000014000A390o
		sub	rsp, 28h
		mov	eax, [r8]
		mov	r9, rcx
		mov	r11d, eax
		mov	r10, rcx
		and	r11d, 0FFFFFFF8h
		test	al, 4
		jz	short loc_140004BE3
		mov	eax, [r8+8]
		movsxd	r10, dword ptr [r8+4]
		neg	eax
		add	r10, rcx
		movsxd	rcx, eax
		and	r10, rcx

loc_140004BE3:				; CODE XREF: sub_140004BB8+16j
		movsxd	rax, r11d
		mov	r8, [rax+r10]
		mov	rax, [rdx+10h]
		mov	ecx, [rax+8]
		mov	rax, [rdx+8]
		mov	dl, [rcx+rax+3]
		test	dl, 0Fh
		jz	short loc_140004C07
		movzx	eax, dl
		and	eax, 0FFFFFFF0h
		add	r9, rax

loc_140004C07:				; CODE XREF: sub_140004BB8+44j
		xor	r9, r8
		mov	rcx, r9		; BugCheckParameter1
		call	sub_140004B50
		add	rsp, 28h
		retn
sub_140004BB8	endp

; ---------------------------------------------------------------------------
algn_140004C17:				; DATA XREF: .pdata:000000014000A390o
		align 20h
; [00000006 BYTES: COLLAPSED FUNCTION __C_specific_handler. PRESS CTRL-NUMPAD+ TO EXPAND]
; [00000006 BYTES: COLLAPSED FUNCTION KeGetProcessorNumberFromIndex. PRESS CTRL-NUMPAD+	TO EXPAND]
		align 10h
; [00000006 BYTES: COLLAPSED FUNCTION strcmp. PRESS CTRL-NUMPAD+ TO EXPAND]
; [00000006 BYTES: COLLAPSED FUNCTION WdfVersionUnbind.	PRESS CTRL-NUMPAD+ TO EXPAND]
; [00000006 BYTES: COLLAPSED FUNCTION WdfVersionBind. PRESS CTRL-NUMPAD+ TO EXPAND]
; [00000006 BYTES: COLLAPSED FUNCTION WdfVersionBindClass. PRESS CTRL-NUMPAD+ TO EXPAND]
; [00000006 BYTES: COLLAPSED FUNCTION WdfVersionUnbindClass. PRESS CTRL-NUMPAD+	TO EXPAND]
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140004C60	proc near		; DATA XREF: .rdata:off_140006138o
					; .pdata:000000014000A39Co
		jmp	rax
sub_140004C60	endp

; ---------------------------------------------------------------------------
algn_140004C62:				; DATA XREF: .pdata:000000014000A39Co
		align 20h

; =============== S U B	R O U T	I N E =======================================


init_memory	proc near		; CODE XREF: sub_140001F74+1Bp
					; sub_14000280C+4Cp ...
		mov	rax, rcx
		cmp	r8, 8
		jb	short loc_140004CB5
		movzx	edx, dl
		mov	r9, 101010101010101h
		imul	rdx, r9
		cmp	r8, 47h
		jnb	short loc_140004D00
		mov	r9, r8
		and	r9, 0FFFFFFFFFFFFFFF8h
		add	rcx, r9

loc_140004CAA:				; CODE XREF: init_memory+33j
		mov	[r9+rax-8], rdx
		sub	r9, 8
		jnz	short loc_140004CAA

loc_140004CB5:				; CODE XREF: init_memory+7j
		and	r8, 7
		jz	short locret_140004CCA
		nop	dword ptr [rax+rax+00h]

loc_140004CC0:				; CODE XREF: init_memory+48j
		mov	[r8+rcx-1], dl
		dec	r8
		jnz	short loc_140004CC0

locret_140004CCA:			; CODE XREF: init_memory+39j
		retn
; ---------------------------------------------------------------------------
		align 40h

loc_140004D00:				; CODE XREF: init_memory+1Ej
		neg	ecx
		and	ecx, 7
		jz	short loc_140004D0D
		sub	r8, rcx
		mov	[rax], rdx

loc_140004D0D:				; CODE XREF: init_memory+85j
		add	rcx, rax
		mov	r9, r8
		shr	r9, 3
		mov	r10, r9
		shr	r10, 3
		and	r9, 7
		jz	short loc_140004D40
		sub	r9, 8
		lea	rcx, [rcx+r9*8]
		neg	r9
		inc	r10
		lea	r11, loc_140004D3D+2
		lea	r11, [r11+r9*4]

loc_140004D3D:				; DATA XREF: init_memory+B2o
		jmp	r11
; ---------------------------------------------------------------------------

loc_140004D40:				; CODE XREF: init_memory+A2j
					; init_memory+E6j
		mov	[rcx], rdx
		mov	[rcx+8], rdx
		mov	[rcx+10h], rdx
		mov	[rcx+18h], rdx
		mov	[rcx+20h], rdx
		mov	[rcx+28h], rdx
		mov	[rcx+30h], rdx
		mov	[rcx+38h], rdx
		add	rcx, 40h
		dec	r10
		jnz	short loc_140004D40
		and	r8, 7
		jz	short locret_140004D78

loc_140004D6E:				; CODE XREF: init_memory+F6j
		mov	[r8+rcx-1], dl
		dec	r8
		jnz	short loc_140004D6E

locret_140004D78:			; CODE XREF: init_memory+ECj
		retn
init_memory	endp

; ---------------------------------------------------------------------------
algn_140004D79:				; DATA XREF: .pdata:000000014000A3A8o
		align 20h

; =============== S U B	R O U T	I N E =======================================


sub_140004D80	proc near		; DATA XREF: .pdata:000000014000A3B4o
		mov	r11, rcx
		sub	rdx, rcx
		jb	loc_140004F2E
		cmp	r8, 4Fh
		jnb	short loc_140004DEA

loc_140004D92:				; CODE XREF: sub_140004D80+BEj
					; sub_140004D80+194j
		mov	r9, r8
		shr	r9, 3
		jz	short loc_140004DB1
		nop	dword ptr [rax+rax+00h]

loc_140004DA0:				; CODE XREF: sub_140004D80+2Fj
		mov	rax, [rdx+rcx]
		add	rcx, 8
		dec	r9
		mov	[rcx-8], rax
		jnz	short loc_140004DA0

loc_140004DB1:				; CODE XREF: sub_140004D80+19j
		and	r8, 7
		jz	short loc_140004DCE
		nop	word ptr [rax+rax+00000000h]

loc_140004DC0:				; CODE XREF: sub_140004D80+4Cj
		mov	al, [rdx+rcx]
		inc	rcx
		dec	r8
		mov	[rcx-1], al
		jnz	short loc_140004DC0

loc_140004DCE:				; CODE XREF: sub_140004D80+35j
		mov	rax, r11
		retn
; ---------------------------------------------------------------------------
		db 6 dup(66h), 0Fh, 1Fh, 84h, 5	dup(0)
		db 0Ah dup(90h)
; ---------------------------------------------------------------------------

loc_140004DEA:				; CODE XREF: sub_140004D80+10j
		cmp	rdx, 10h
		jb	short loc_140004E60
		neg	ecx
		and	ecx, 0Fh
		jz	short loc_140004E05
		sub	r8, rcx
		movdqu	xmm0, xmmword ptr [rdx+r11]
		movdqu	xmmword	ptr [r11], xmm0

loc_140004E05:				; CODE XREF: sub_140004D80+75j
		add	rcx, r11

loc_140004E08:				; CODE XREF: sub_140004D80+E3j
					; sub_140004D80+F5j
		mov	r9, r8
		shr	r9, 5
		cmp	r9, 2000h
		ja	loc_140004E92

loc_140004E1C:				; CODE XREF: sub_140004D80+119j
					; sub_140004D80+18Ej
		and	r8, 1Fh

loc_140004E20:				; CODE XREF: sub_140004D80+BCj
		movdqu	xmm0, xmmword ptr [rdx+rcx]
		movdqu	xmm1, xmmword ptr [rdx+rcx+10h]
		add	rcx, 20h
		movdqa	xmmword	ptr [rcx-20h], xmm0
		movdqa	xmmword	ptr [rcx-10h], xmm1
		dec	r9
		jnz	short loc_140004E20
		jmp	loc_140004D92
; ---------------------------------------------------------------------------
		align 20h

loc_140004E60:				; CODE XREF: sub_140004D80+6Ej
		test	cl, 0Fh
		jz	short loc_140004E08

loc_140004E65:				; CODE XREF: sub_140004D80+F3j
		mov	al, [rdx+rcx]
		dec	r8
		mov	[rcx], al
		inc	rcx
		test	cl, 0Fh
		jnz	short loc_140004E65
		jmp	short loc_140004E08
; ---------------------------------------------------------------------------
		db 66h,	0Fh, 1Fh, 84h, 5 dup(0)
		db 12h dup(90h)
; ---------------------------------------------------------------------------

loc_140004E92:				; CODE XREF: sub_140004D80+96j
		cmp	rdx, 200h
		jb	short loc_140004E1C

loc_140004E9B:				; CODE XREF: sub_140004D80+180j
		mov	eax, 4

loc_140004EA0:				; CODE XREF: sub_140004D80+132j
		prefetchnta byte ptr [rdx+rcx]
		prefetchnta byte ptr [rdx+rcx+40h]
		add	rcx, 80h
		dec	eax
		jnz	short loc_140004EA0
		sub	rcx, 200h
		mov	eax, 8

loc_140004EC0:				; CODE XREF: sub_140004D80+170j
		movdqu	xmm0, xmmword ptr [rdx+rcx]
		movdqu	xmm1, xmmword ptr [rdx+rcx+10h]
		movntdq	xmmword	ptr [rcx], xmm0
		movntdq	xmmword	ptr [rcx+10h], xmm1
		add	rcx, 40h
		movdqu	xmm0, xmmword ptr [rdx+rcx-20h]
		movdqu	xmm1, xmmword ptr [rdx+rcx-10h]
		movntdq	xmmword	ptr [rcx-20h], xmm0
		movntdq	xmmword	ptr [rcx-10h], xmm1
		dec	eax
		jnz	short loc_140004EC0
		sub	r8, 200h
		cmp	r8, 200h
		jnb	short loc_140004E9B
		lock or	byte ptr [rsp+0], 0
		mov	r9, r8
		shr	r9, 5
		jnz	loc_140004E1C
		jmp	loc_140004D92
; ---------------------------------------------------------------------------
		db 0Fh,	1Fh, 80h, 4 dup(0)
		db 0Eh dup(90h)
; ---------------------------------------------------------------------------

loc_140004F2E:				; CODE XREF: sub_140004D80+6j
		add	rcx, r8
		cmp	r8, 4Fh
		jnb	short loc_140004F86

loc_140004F37:				; CODE XREF: sub_140004D80+25Ej
					; sub_140004D80+334j
		mov	r9, r8
		shr	r9, 3
		jz	short loc_140004F51

loc_140004F40:				; CODE XREF: sub_140004D80+1CFj
		mov	rax, [rdx+rcx-8]
		sub	rcx, 8
		dec	r9
		mov	[rcx], rax
		jnz	short loc_140004F40

loc_140004F51:				; CODE XREF: sub_140004D80+1BEj
		and	r8, 7
		jz	short loc_140004F6E
		nop	word ptr [rax+rax+00000000h]

loc_140004F60:				; CODE XREF: sub_140004D80+1ECj
		mov	al, [rdx+rcx-1]
		dec	rcx
		dec	r8
		mov	[rcx], al
		jnz	short loc_140004F60

loc_140004F6E:				; CODE XREF: sub_140004D80+1D5j
		mov	rax, r11
		retn
; ---------------------------------------------------------------------------
		db 6 dup(66h), 0Fh, 1Fh, 84h, 5	dup(0)
		db 6 dup(90h)
; ---------------------------------------------------------------------------

loc_140004F86:				; CODE XREF: sub_140004D80+1B5j
		cmp	rdx, 0FFFFFFFFFFFFFFF0h
		ja	short loc_140005000
		mov	rax, rcx
		and	ecx, 0Fh
		jz	short loc_140004FA5
		sub	r8, rcx
		neg	rcx
		movdqu	xmm0, xmmword ptr [rdx+rax-10h]
		movdqu	xmmword	ptr [rax-10h], xmm0

loc_140004FA5:				; CODE XREF: sub_140004D80+212j
		add	rcx, rax

loc_140004FA8:				; CODE XREF: sub_140004D80+283j
					; sub_140004D80+295j
		mov	r9, r8
		shr	r9, 5
		cmp	r9, 2000h
		ja	loc_140005032

loc_140004FBC:				; CODE XREF: sub_140004D80+2B9j
					; sub_140004D80+32Ej
		and	r8, 1Fh

loc_140004FC0:				; CODE XREF: sub_140004D80+25Cj
		movdqu	xmm0, xmmword ptr [rdx+rcx-10h]
		movdqu	xmm1, xmmword ptr [rdx+rcx-20h]
		sub	rcx, 20h
		movdqa	xmmword	ptr [rcx+10h], xmm0
		movdqa	xmmword	ptr [rcx], xmm1
		dec	r9
		jnz	short loc_140004FC0
		jmp	loc_140004F37
; ---------------------------------------------------------------------------
		align 20h

loc_140005000:				; CODE XREF: sub_140004D80+20Aj
		test	cl, 0Fh
		jz	short loc_140004FA8

loc_140005005:				; CODE XREF: sub_140004D80+293j
		dec	rcx
		mov	al, [rdx+rcx]
		dec	r8
		mov	[rcx], al
		test	cl, 0Fh
		jnz	short loc_140005005
		jmp	short loc_140004FA8
; ---------------------------------------------------------------------------
		db 66h,	0Fh, 1Fh, 84h, 5 dup(0)
		db 12h dup(90h)
; ---------------------------------------------------------------------------

loc_140005032:				; CODE XREF: sub_140004D80+236j
		cmp	rdx, 0FFFFFFFFFFFFFE00h
		ja	short loc_140004FBC

loc_14000503B:				; CODE XREF: sub_140004D80+320j
		mov	eax, 4

loc_140005040:				; CODE XREF: sub_140004D80+2D2j
		sub	rcx, 80h
		prefetchnta byte ptr [rdx+rcx]
		prefetchnta byte ptr [rdx+rcx+40h]
		dec	eax
		jnz	short loc_140005040
		add	rcx, 200h
		mov	eax, 8

loc_140005060:				; CODE XREF: sub_140004D80+310j
		movdqu	xmm0, xmmword ptr [rdx+rcx-10h]
		movdqu	xmm1, xmmword ptr [rdx+rcx-20h]
		movntdq	xmmword	ptr [rcx-10h], xmm0
		movntdq	xmmword	ptr [rcx-20h], xmm1
		sub	rcx, 40h
		movdqu	xmm0, xmmword ptr [rdx+rcx+10h]
		movdqu	xmm1, xmmword ptr [rdx+rcx]
		movntdq	xmmword	ptr [rcx+10h], xmm0
		movntdq	xmmword	ptr [rcx], xmm1
		dec	eax
		jnz	short loc_140005060
		sub	r8, 200h
		cmp	r8, 200h
		jnb	short loc_14000503B
		lock or	byte ptr [rsp+0], 0
		mov	r9, r8
		shr	r9, 5
		jnz	loc_140004FBC
		jmp	loc_140004F37
sub_140004D80	endp

; ---------------------------------------------------------------------------
algn_1400050B9:				; DATA XREF: .pdata:000000014000A3B4o
		align 20h
; char Str2[]
Str2		db '.text',0            ; DATA XREF: do_something_to_text_seg+54o

; =============== S U B	R O U T	I N E =======================================


sub_1400050C6	proc near		; DATA XREF: .rdata:0000000140006570o
					; .pdata:000000014000A3C0o
		push	rbp
		sub	rsp, 20h
		mov	rbp, rdx
		mov	rax, [rbp+38h]
		mov	cr3, rax
		add	rsp, 20h
		pop	rbp
		retn
sub_1400050C6	endp

; ---------------------------------------------------------------------------
		db 0CCh

; =============== S U B	R O U T	I N E =======================================


sub_1400050DD	proc near		; DATA XREF: .rdata:0000000140006968o
					; .pdata:000000014000A3C0o ...
		push	rbp
		sub	rsp, 30h
		mov	rbp, rdx
		add	rsp, 30h
		pop	rbp
		retn
sub_1400050DD	endp

; ---------------------------------------------------------------------------
		db 0CCh

; =============== S U B	R O U T	I N E =======================================


sub_1400050ED	proc near		; DATA XREF: .rdata:00000001400069A8o
					; .pdata:000000014000A3CCo ...
		push	rbp
		sub	rsp, 20h
		mov	rbp, rdx
		add	rsp, 20h
		pop	rbp
		retn
sub_1400050ED	endp

; ---------------------------------------------------------------------------
algn_1400050FC:				; DATA XREF: .pdata:000000014000A3D8o
		align 200h
		dq 1C0h	dup(?)
_text		ends

; Section 2. (virtual address 00006000)
; Virtual size			: 00000A24 (   2596.)
; Section size in file		: 00000C00 (   3072.)
; Offset to raw	data for section: 00004600
; Flags	48000040: Data Not pageable Readable
; Alignment	: default
;
; Imports from WDFLDR.SYS
;
; ===========================================================================

; Segment type:	Externs
; _idata
		extrn __imp_WdfVersionBind:qword ; DATA	XREF: WdfVersionBindr
					; INIT:000000014000D594o
		extrn __imp_WdfVersionUnbind:qword ; DATA XREF:	WdfVersionUnbindr
		extrn __imp_WdfVersionUnbindClass:qword	; DATA XREF: WdfVersionUnbindClassr
		extrn __imp_WdfVersionBindClass:qword ;	DATA XREF: WdfVersionBindClassr

;
; Imports from ntoskrnl.exe
;
		extrn KeGetCurrentProcessorNumberEx:qword ; CODE XREF: sub_140003144+11Dp
					; real_handler+6Ep ...
; PVOID	__stdcall ExAllocatePoolWithTag(POOL_TYPE PoolType, SIZE_T NumberOfBytes, ULONG	Tag)
		extrn ExAllocatePoolWithTag:qword ; CODE XREF: sub_14000280C+33p
					; init_CSTRUCT_0x20+2Ep ...
; void __stdcall ExFreePoolWithTag(PVOID P, ULONG Tag)
		extrn ExFreePoolWithTag:qword ;	CODE XREF: sub_1400027C4+2Bp
					; sub_1400029E4+6Dp ...
; NTSTATUS __stdcall ExDeleteResourceLite(PERESOURCE Resource)
		extrn ExDeleteResourceLite:qword ; CODE	XREF: sub_14000B000+B1p
					; DATA XREF: sub_14000B000+B1r
; PVOID	__stdcall MmGetSystemRoutineAddress(PUNICODE_STRING SystemRoutineName)
		extrn MmGetSystemRoutineAddress:qword ;	CODE XREF: get_routine_address+23p
					; DATA XREF: get_routine_address+23r
; NTSTATUS __stdcall ZwClose(HANDLE Handle)
		extrn ZwClose:qword	; CODE XREF: sub_14000B000+50p
					; sub_14000B000+67p
					; DATA XREF: ...
		extrn ZwWaitForSingleObject:qword ; CODE XREF: sub_14000B000+3Ap
					; DATA XREF: sub_14000B000+3Ar
; PBOOLEAN KdDebuggerNotPresent
		extrn KdDebuggerNotPresent:qword ; DATA	XREF: sub_140001588r
					; sub_1400026C4+BAr ...
		extrn __imp___C_specific_handler:qword ; DATA XREF: __C_specific_handlerr
		extrn RtlGetVersion:qword ; CODE XREF: main_run_stuff+3Ap
					; more_version_check+30p ...
; SIZE_T __stdcall RtlCompareMemory(const void *Source1, const void *Source2, SIZE_T Length)
		extrn RtlCompareMemory:qword ; CODE XREF: find_substring_pos+3Dp
					; DATA XREF: find_substring_pos+3Dr
		extrn KeSetSystemGroupAffinityThread:qword
					; CODE XREF: execute_func_on_each_proc+7Dp
					; DATA XREF: execute_func_on_each_proc+7Dr
		extrn KeRevertToUserGroupAffinityThread:qword
					; CODE XREF: execute_func_on_each_proc+8Fp
					; DATA XREF: execute_func_on_each_proc+8Fr
		extrn KeQueryActiveProcessorCountEx:qword
					; CODE XREF: execute_func_on_each_proc+2Cp
					; DATA XREF: execute_func_on_each_proc+2Cr
		extrn __imp_KeGetProcessorNumberFromIndex:qword
					; DATA XREF: KeGetProcessorNumberFromIndexr
; PVOID	__stdcall MmMapLockedPagesSpecifyCache(PMDL MemoryDescriptorList, KPROCESSOR_MODE AccessMode, MEMORY_CACHING_TYPE CacheType, PVOID BaseAddress,	ULONG BugCheckOnFailure, MM_PAGE_PRIORITY Priority)
		extrn MmMapLockedPagesSpecifyCache:qword ; CODE	XREF: allocate_stuff+6Dp
					; DATA XREF: allocate_stuff+6Dr
		extrn MmAllocateContiguousMemory:qword ; DATA XREF: INIT_HOST_RSP+3Br
		extrn __imp_MmFreeContiguousMemory:qword
					; DATA XREF: MmFreeContiguousMemoryr
; PMDL __stdcall IoAllocateMdl(PVOID VirtualAddress, ULONG Length, BOOLEAN SecondaryBuffer, BOOLEAN ChargeQuota, PIRP Irp)
		extrn IoAllocateMdl:qword ; CODE XREF: allocate_stuff+1Fp
					; DATA XREF: allocate_stuff+1Fr
; void __stdcall IoFreeMdl(PMDL	Mdl)
		extrn IoFreeMdl:qword	; CODE XREF: allocate_stuff+84p
					; allocate_stuff+9Cp
					; DATA XREF: ...
		extrn MmGetPhysicalMemoryRanges:qword ;	CODE XREF: sub_14000D36C+19p
					; DATA XREF: sub_14000D36C+19r
		extrn __imp_MmGetPhysicalAddress:qword ; CODE XREF: sub_140002E3C+47p
					; DATA XREF: sub_140002E3C+47r	...
		extrn MmGetVirtualForPhysical:qword ; DATA XREF: sub_140002F8C+4r
		extrn MmSystemRangeStart:qword ; DATA XREF: sub_140002FE4r
; void __stdcall RtlInitializeBitMap(PRTL_BITMAP BitMapHeader, PULONG BitMapBuffer, ULONG SizeOfBitMap)
		extrn RtlInitializeBitMap:qword	; CODE XREF: sub_14000B82C+8Ap
					; sub_14000B82C+FAp ...
; void __stdcall RtlClearBits(PRTL_BITMAP BitMapHeader,	ULONG StartingIndex, ULONG NumberToClear)
		extrn RtlClearBits:qword ; CODE	XREF: sub_14000B82C+A0p
					; sub_14000B82C+CCp ...
; void __stdcall MmProbeAndLockPages(PMDL MemoryDescriptorList,	KPROCESSOR_MODE	AccessMode, LOCK_OPERATION Operation)
		extrn MmProbeAndLockPages:qword	; CODE XREF: allocate_stuff+41p
					; DATA XREF: allocate_stuff+41r
; void __stdcall MmUnlockPages(PMDL MemoryDescriptorList)
		extrn MmUnlockPages:qword ; CODE XREF: VMCALL_HANDLER+A8Ap
					; allocate_stuff+7Bp
					; DATA XREF: ...
; int __cdecl strcmp(const char	*Str1, const char *Str2)
		extrn __imp_strcmp:qword ; DATA	XREF: strcmpr
; void __stdcall __noreturn KeBugCheckEx(ULONG BugCheckCode, ULONG_PTR BugCheckParameter1, ULONG_PTR BugCheckParameter2, ULONG_PTR BugCheckParameter3, ULONG_PTR BugCheckParameter4)
		extrn KeBugCheckEx:qword ; CODE	XREF: sub_140004B50+40p
					; DATA XREF: sub_140004B50+40r
; void __stdcall RtlCopyUnicodeString(PUNICODE_STRING DestinationString, PCUNICODE_STRING SourceString)
		extrn RtlCopyUnicodeString:qword ; CODE	XREF: drivermain+5Cp
					; DATA XREF: drivermain+5Cr
; void __stdcall RtlInitUnicodeString(PUNICODE_STRING DestinationString, PCWSTR	SourceString)
		extrn RtlInitUnicodeString:qword ; CODE	XREF: get_routine_address+18p
					; DATA XREF: get_routine_address+18r


; ===========================================================================

; Segment type:	Pure data
; Segment permissions: Read
_rdata		segment	para public 'DATA' use64
		assume cs:_rdata
		;org 140006130h
__guard_check_icall_fptr dq offset nullsub_1 ; DATA XREF: .rdata:0000000140006230o
off_140006138	dq offset sub_140004C60	; DATA XREF: .rdata:0000000140006238o
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
unk_140006148	db    0			; DATA XREF: no_cb_called+Ao
					; no_cb_called+11o
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
some_func_preambule db	48h ; H		; DATA XREF: set_func_and_page_table_pointers+8Bo
		db  8Bh	; ã
		db    4
		db 0D0h	; –
		db  48h	; H
		db 0C1h	; ¡
		db 0E0h	; ‡
		db  19h
		db  48h	; H
		db 0BAh	; ∫
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
aKmdflibrary:				; DATA XREF: .data:0000000140007038o
		unicode	0, <KmdfLibrary>,0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
; Debug	Directory entries
		dd 0			; Characteristics
		dd 5B5375D8h		; TimeDateStamp: Sat Jul 21 18:05:12 2018
		dw 0			; MajorVersion
		dw 0			; MinorVersion
		dd 2			; Type:	IMAGE_DEBUG_TYPE_CODEVIEW
		dd 6Ah			; SizeOfData
		dd rva asc_1400062C0	; AddressOfRawData
		dd 48C0h		; PointerToRawData
		dd 0			; Characteristics
		dd 5B5375D8h		; TimeDateStamp: Sat Jul 21 18:05:12 2018
		dw 0			; MajorVersion
		dw 0			; MinorVersion
		dd 0Dh			; Type
		dd 228h			; SizeOfData
		dd rva unk_14000632C	; AddressOfRawData
		dd 492Ch		; PointerToRawData
		align 20h
_load_config_used dd 100h		; Size
		dd 0			; Time stamp
		dw 2 dup(0)		; Version: 0.0
		dd 0			; GlobalFlagsClear
		dd 0			; GlobalFlagsSet
		dd 0			; CriticalSectionDefaultTimeout
		dq 0			; DeCommitFreeBlockThreshold
		dq 0			; DeCommitTotalFreeThreshold
		dq 0			; LockPrefixTable
		dq 0			; MaximumAllocationSize
		dq 0			; VirtualMemoryThreshold
		dq 0			; ProcessAffinityMask
		dd 0			; ProcessHeapFlags
		dw 0			; CSDVersion
		dw 0			; Reserved1
		dq 0			; EditList
		dq offset __security_cookie ; SecurityCookie
		dq 0			; SEHandlerTable
		dq 0			; SEHandlerCount
		dq offset __guard_check_icall_fptr ; GuardCFCheckFunctionPointer
		dq offset off_140006138	; Reserved2
		dq 0			; GuardCFFunctionTable
		dq 0			; GuardCFFunctionCount
		dd 100h			; GuardFlags
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
; Debug	information (IMAGE_DEBUG_TYPE_CODEVIEW)
asc_1400062C0	db 'RSDS'               ; DATA XREF: .rdata:0000000140006194o
					; CV signature
		dd 0DFD6FA3Ch		; Data1	; GUID
		dw 0CCB6h		; Data2
		dw 4362h		; Data3
		db 86h,	0BFh, 0F6h, 76h, 0D1h, 63h, 0C3h, 55h; Data4
		dd 1			; Age
		db 'ASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASDASD\t' ; PdbFileName
		db 'oobadsoosadd.pdb',0
		align 4
; Debug	information (type 13)
unk_14000632C	db    0			; DATA XREF: .rdata:00000001400061B0o
		db    0
		db    0
		db    0
		db    0
		db  10h
		db    0
		db    0
		db  20h
		db    3
		db    0
		db    0
		db  2Eh	; .
		db  74h	; t
		db  65h	; e
		db  78h	; x
		db  74h	; t
		db    0
		db    0
		db    0
		db  20h
		db  13h
		db    0
		db    0
		db  30h	; 0
		db  39h	; 9
		db    0
		db    0
		db  2Eh	; .
		db  74h	; t
		db  65h	; e
		db  78h	; x
		db  74h	; t
		db  24h	; $
		db  6Dh	; m
		db  6Eh	; n
		db    0
		db    0
		db    0
		db    0
		db  50h	; P
		db  4Ch	; L
		db    0
		db    0
		db  30h	; 0
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  74h	; t
		db  65h	; e
		db  78h	; x
		db  74h	; t
		db  24h	; $
		db  6Dh	; m
		db  6Eh	; n
		db  24h	; $
		db  30h	; 0
		db  30h	; 0
		db    0
		db  80h	; Ä
		db  4Ch	; L
		db    0
		db    0
		db  40h	; @
		db    4
		db    0
		db    0
		db  2Eh	; .
		db  74h	; t
		db  65h	; e
		db  78h	; x
		db  74h	; t
		db  24h	; $
		db  6Dh	; m
		db  6Eh	; n
		db  24h	; $
		db  32h	; 2
		db  31h	; 1
		db    0
		db 0C0h	; ¿
		db  50h	; P
		db    0
		db    0
		db    6
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  74h	; t
		db  65h	; e
		db  78h	; x
		db  74h	; t
		db  24h	; $
		db  73h	; s
		db    0
		db 0C6h	; ∆
		db  50h	; P
		db    0
		db    0
		db  37h	; 7
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  74h	; t
		db  65h	; e
		db  78h	; x
		db  74h	; t
		db  24h	; $
		db  78h	; x
		db    0
		db    0
		db  60h	; `
		db    0
		db    0
		db  30h	; 0
		db    1
		db    0
		db    0
		db  2Eh	; .
		db  69h	; i
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db  24h	; $
		db  35h	; 5
		db    0
		db    0
		db    0
		db    0
		db  30h	; 0
		db  61h	; a
		db    0
		db    0
		db  10h
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  30h	; 0
		db  30h	; 0
		db  63h	; c
		db  66h	; f
		db  67h	; g
		db    0
		db    0
		db  40h	; @
		db  61h	; a
		db    0
		db    0
		db    8
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  43h	; C
		db  52h	; R
		db  54h	; T
		db  24h	; $
		db  58h	; X
		db  43h	; C
		db  41h	; A
		db    0
		db    0
		db    0
		db    0
		db  48h	; H
		db  61h	; a
		db    0
		db    0
		db    8
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  43h	; C
		db  52h	; R
		db  54h	; T
		db  24h	; $
		db  58h	; X
		db  43h	; C
		db  5Ah	; Z
		db    0
		db    0
		db    0
		db    0
		db  50h	; P
		db  61h	; a
		db    0
		db    0
		db  70h	; p
		db    1
		db    0
		db    0
		db  2Eh	; .
		db  72h	; r
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db    0
		db    0
		db 0C0h	; ¿
		db  62h	; b
		db    0
		db    0
		db  98h	; ò
		db    2
		db    0
		db    0
		db  2Eh	; .
		db  72h	; r
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db  24h	; $
		db  7Ah	; z
		db  7Ah	; z
		db  7Ah	; z
		db  64h	; d
		db  62h	; b
		db  67h	; g
		db    0
		db    0
		db    0
		db  58h	; X
		db  65h	; e
		db    0
		db    0
		db 0CCh	; Ã
		db    4
		db    0
		db    0
		db  2Eh	; .
		db  78h	; x
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db    0
		db    0
		db    0
		db  70h	; p
		db    0
		db    0
		db  60h	; `
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db    0
		db    0
		db    0
		db  60h	; `
		db  70h	; p
		db    0
		db    0
		db  10h
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  6Bh	; k
		db  6Dh	; m
		db  64h	; d
		db  66h	; f
		db  63h	; c
		db  6Ch	; l
		db  61h	; a
		db  73h	; s
		db  73h	; s
		db  62h	; b
		db  69h	; i
		db  6Eh	; n
		db  64h	; d
		db  24h	; $
		db  61h	; a
		db    0
		db    0
		db    0
		db    0
		db  70h	; p
		db  70h	; p
		db    0
		db    0
		db    8
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  6Bh	; k
		db  6Dh	; m
		db  64h	; d
		db  66h	; f
		db  63h	; c
		db  6Ch	; l
		db  61h	; a
		db  73h	; s
		db  73h	; s
		db  62h	; b
		db  69h	; i
		db  6Eh	; n
		db  64h	; d
		db  24h	; $
		db  63h	; c
		db    0
		db    0
		db    0
		db    0
		db  78h	; x
		db  70h	; p
		db    0
		db    0
		db    8
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  6Bh	; k
		db  6Dh	; m
		db  64h	; d
		db  66h	; f
		db  63h	; c
		db  6Ch	; l
		db  61h	; a
		db  73h	; s
		db  73h	; s
		db  62h	; b
		db  69h	; i
		db  6Eh	; n
		db  64h	; d
		db  24h	; $
		db  64h	; d
		db    0
		db    0
		db    0
		db    0
		db  80h	; Ä
		db  70h	; p
		db    0
		db    0
		db  10h
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  6Bh	; k
		db  6Dh	; m
		db  64h	; d
		db  66h	; f
		db  74h	; t
		db  79h	; y
		db  70h	; p
		db  65h	; e
		db  69h	; i
		db  6Eh	; n
		db  69h	; i
		db  74h	; t
		db  24h	; $
		db  61h	; a
		db    0
		db  90h	; ê
		db  70h	; p
		db    0
		db    0
		db  10h
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  6Bh	; k
		db  6Dh	; m
		db  64h	; d
		db  66h	; f
		db  74h	; t
		db  79h	; y
		db  70h	; p
		db  65h	; e
		db  69h	; i
		db  6Eh	; n
		db  69h	; i
		db  74h	; t
		db  24h	; $
		db  63h	; c
		db    0
		db 0A0h	; †
		db  70h	; p
		db    0
		db    0
		db 0C8h	; »
		db  2Ah	; *
		db    0
		db    0
		db  2Eh	; .
		db  62h	; b
		db  73h	; s
		db  73h	; s
		db    0
		db    0
		db    0
		db    0
		db    0
		db 0A0h	; †
		db    0
		db    0
		db  10h
		db    5
		db    0
		db    0
		db  2Eh	; .
		db  70h	; p
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db    0
		db    0
		db    0
		db 0B0h	; ∞
		db    0
		db    0
		db  7Ch	; |
		db  16h
		db    0
		db    0
		db  50h	; P
		db  41h	; A
		db  47h	; G
		db  45h	; E
		db    0
		db    0
		db    0
		db    0
		db    0
		db 0D0h	; –
		db    0
		db    0
		db    0
		db    5
		db    0
		db    0
		db  49h	; I
		db  4Eh	; N
		db  49h	; I
		db  54h	; T
		db    0
		db    0
		db    0
		db    0
		db    0
		db 0D5h	; ’
		db    0
		db    0
		db  70h	; p
		db    0
		db    0
		db    0
		db  49h	; I
		db  4Eh	; N
		db  49h	; I
		db  54h	; T
		db  24h	; $
		db  73h	; s
		db    0
		db    0
		db  70h	; p
		db 0D5h	; ’
		db    0
		db    0
		db  28h	; (
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  69h	; i
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db  24h	; $
		db  32h	; 2
		db    0
		db    0
		db    0
		db    0
		db  98h	; ò
		db 0D5h	; ’
		db    0
		db    0
		db  18h
		db    0
		db    0
		db    0
		db  2Eh	; .
		db  69h	; i
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db  24h	; $
		db  33h	; 3
		db    0
		db    0
		db    0
		db    0
		db 0B0h	; ∞
		db 0D5h	; ’
		db    0
		db    0
		db  30h	; 0
		db    1
		db    0
		db    0
		db  2Eh	; .
		db  69h	; i
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db  24h	; $
		db  34h	; 4
		db    0
		db    0
		db    0
		db    0
		db 0E0h	; ‡
		db 0D6h	; ÷
		db    0
		db    0
		db  58h	; X
		db    3
		db    0
		db    0
		db  2Eh	; .
		db  69h	; i
		db  64h	; d
		db  61h	; a
		db  74h	; t
		db  61h	; a
		db  24h	; $
		db  36h	; 6
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
stru_140006558	UNWIND_INFO <12h, 0Ah, 6, 0> ; DATA XREF: .pdata:000000014000A1E0o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Ah, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Ah, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
		dd rva __C_specific_handler
		dd 1
		C_SCOPE_TABLE <rva loc_1400023CB, rva loc_140002698, \
			       rva sub_1400050C6, 0>
stru_140006580	UNWIND_INFO <2,	0Ah, 6,	0> ; DATA XREF:	.pdata:000000014000A060o
					; .pdata:000000014000A078o ...
		UNWIND_CODE <6,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Ah, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Ah, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
stru_140006590	UNWIND_INFO <2,	15h, 0Ah, 0> ; DATA XREF: .pdata:000000014000A0A8o
					; .pdata:000000014000A0B4o
		UNWIND_CODE <7,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <15h, 74h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <15h, 64h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <15h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <15h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <11h, 0E0h>	; UWOP_PUSH_NONVOL
stru_1400065A8	UNWIND_INFO <2,	19h, 0Ch, 0> ; DATA XREF: .pdata:000000014000A0C0o
		UNWIND_CODE <7,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <19h, 0E4h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <19h, 74h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <19h, 64h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <19h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <19h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <15h, 0F0h>	; UWOP_PUSH_NONVOL
stru_1400065C4	UNWIND_INFO <2,	0Fh, 8,	0> ; DATA XREF:	.pdata:000000014000A054o
					; .pdata:000000014000A084o ...
		UNWIND_CODE <6,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Fh, 64h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <0Fh, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Fh, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
stru_1400065D8	UNWIND_INFO <2,	6, 4, 0> ; DATA	XREF: .pdata:000000014000A06Co
					; .pdata:000000014000A144o ...
		UNWIND_CODE <6,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <6,	32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <2,	30h>	; UWOP_PUSH_NONVOL
stru_1400065E4	UNWIND_INFO <2,	19h, 0Ch, 0> ; DATA XREF: .pdata:000000014000A114o
					; .pdata:000000014000A300o ...
		UNWIND_CODE <7,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <19h, 74h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <19h, 64h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <19h, 54h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <19h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <19h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <15h, 0E0h>	; UWOP_PUSH_NONVOL
stru_140006600	UNWIND_INFO <2,	1Dh, 0Eh, 0> ; DATA XREF: .pdata:000000014000A108o
					; .pdata:000000014000A120o
		UNWIND_CODE <0Bh, 16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <1Dh, 74h>	; UWOP_SAVE_NONVOL
		dw 0Bh
		UNWIND_CODE <1Dh, 64h>	; UWOP_SAVE_NONVOL
		dw 0Ah
		UNWIND_CODE <1Dh, 54h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <1Dh, 34h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <1Dh, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <19h, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <17h, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <15h, 0D0h>	; UWOP_PUSH_NONVOL
stru_140006620	UNWIND_INFO <1Ah, 1Fh, 7, 0> ; DATA XREF: .pdata:000000014000A4D4o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Dh, 34h>	; UWOP_SAVE_NONVOL
		dw 2Dh
		UNWIND_CODE <0Dh, 1>	; UWOP_ALLOC_LARGE
		dw 2Ah
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
		align 4
		dd rva sub_140004B98
		dd 140h
stru_14000663C	UNWIND_INFO <2,	4, 3, 0> ; DATA	XREF: .pdata:000000014000A3F0o
		UNWIND_CODE <5,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <4,	42h>	; UWOP_ALLOC_SMALL
		align 4
stru_140006648	UNWIND_INFO <1Ah, 19h, 4, 0> ; DATA XREF: .pdata:000000014000A4E0o
		UNWIND_CODE <1,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <7,	1>	; UWOP_ALLOC_LARGE
		dw 2Bh
		dd rva sub_140004B98
		dd 140h
stru_14000665C	UNWIND_INFO <1Ah, 2Ch, 0Eh, 0> ; DATA XREF: .pdata:000000014000A408o
		UNWIND_CODE <7,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <1Dh, 74h>	; UWOP_SAVE_NONVOL
		dw 0Dh
		UNWIND_CODE <1Dh, 64h>	; UWOP_SAVE_NONVOL
		dw 0Ch
		UNWIND_CODE <1Dh, 54h>	; UWOP_SAVE_NONVOL
		dw 0Bh
		UNWIND_CODE <1Dh, 34h>	; UWOP_SAVE_NONVOL
		dw 0Ah
		UNWIND_CODE <1Dh, 52h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <19h, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <17h, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <15h, 0D0h>	; UWOP_PUSH_NONVOL
		dd rva sub_140004B98
		dd 28h
stru_140006684	UNWIND_INFO <2,	1Ch, 0Eh, 0> ; DATA XREF: .pdata:000000014000A3FCo
		UNWIND_CODE <0Ah, 16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <1Ch, 64h>	; UWOP_SAVE_NONVOL
		dw 0Ch
		UNWIND_CODE <1Ch, 54h>	; UWOP_SAVE_NONVOL
		dw 0Bh
		UNWIND_CODE <1Ch, 34h>	; UWOP_SAVE_NONVOL
		dw 0Ah
		UNWIND_CODE <1Ch, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <18h, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <16h, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <14h, 0D0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <12h, 0C0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <10h, 70h>	; UWOP_PUSH_NONVOL
stru_1400066A4	UNWIND_INFO <2,	6, 4, 0> ; DATA	XREF: .pdata:000000014000A1F8o
		UNWIND_CODE <8,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <6,	32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <2,	30h>	; UWOP_PUSH_NONVOL
stru_1400066B0	UNWIND_INFO <2,	18h, 0Ch, 0> ; DATA XREF: .pdata:000000014000A210o
		UNWIND_CODE <6,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <18h, 64h>	; UWOP_SAVE_NONVOL
		dw 0Ah
		UNWIND_CODE <18h, 54h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <18h, 34h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <18h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <14h, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <12h, 0C0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <10h, 70h>	; UWOP_PUSH_NONVOL
stru_1400066CC	UNWIND_INFO <2,	14h, 0Ah, 0> ; DATA XREF: .pdata:000000014000A21Co
		UNWIND_CODE <8,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <14h, 64h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <14h, 54h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <14h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <14h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <10h, 70h>	; UWOP_PUSH_NONVOL
stru_1400066E4	UNWIND_INFO <2,	0Ah, 6,	0> ; DATA XREF:	.pdata:000000014000A204o
					; .pdata:000000014000A2D0o ...
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Ah, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Ah, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
stru_1400066F4	UNWIND_INFO <2,	0Fh, 8,	0> ; DATA XREF:	.pdata:000000014000A24Co
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Fh, 64h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <0Fh, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Fh, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
stru_140006708	UNWIND_INFO <2,	14h, 0Ah, 0> ; DATA XREF: .pdata:000000014000A234o
		UNWIND_CODE <2,	6>	; UWOP_EPILOG
		UNWIND_CODE <1Eh, 6>	; UWOP_EPILOG
		UNWIND_CODE <14h, 64h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <14h, 54h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <14h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <14h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <10h, 70h>	; UWOP_PUSH_NONVOL
stru_140006720	UNWIND_INFO <2,	0Fh, 8,	0> ; DATA XREF:	.pdata:000000014000A228o
		UNWIND_CODE <8,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Fh, 64h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <0Fh, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Fh, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
stru_140006734	UNWIND_INFO <1Ah, 1Fh, 7, 0> ; DATA XREF: .pdata:000000014000A4F8o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Dh, 34h>	; UWOP_SAVE_NONVOL
		dw 2Ch
		UNWIND_CODE <0Dh, 1>	; UWOP_ALLOC_LARGE
		dw 2Ah
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
		align 4
		dd rva sub_140004B98
		dd 140h
stru_140006750	UNWIND_INFO <1Ah, 21h, 0Ah, 0> ; DATA XREF: .pdata:000000014000A42Co
		UNWIND_CODE <8,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Ch, 6>	; UWOP_EPILOG
		UNWIND_CODE <13h, 34h>	; UWOP_SAVE_NONVOL
		dw 12h
		UNWIND_CODE <13h, 92h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Ch, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <0Ah, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <8,	70h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <7,	60h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <6,	50h>	; UWOP_PUSH_NONVOL
		dd rva sub_140004B98
		dd 48h
stru_140006770	UNWIND_INFO <2,	19h, 0Ch, 0> ; DATA XREF: .pdata:000000014000A1ECo
					; .pdata:000000014000A2A0o
		UNWIND_CODE <3,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <19h, 74h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <19h, 64h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <19h, 54h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <19h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <19h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <15h, 0E0h>	; UWOP_PUSH_NONVOL
stru_14000678C	UNWIND_INFO <2,	4, 3, 0> ; DATA	XREF: .pdata:000000014000A438o
		UNWIND_CODE <1,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <4,	62h>	; UWOP_ALLOC_SMALL
		align 4
stru_140006798	UNWIND_INFO <2,	4, 5, 0> ; DATA	XREF: .pdata:000000014000A258o
		UNWIND_CODE <1,	6>	; UWOP_EPILOG
		UNWIND_CODE <7,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Fh, 6>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <4,	62h>	; UWOP_ALLOC_SMALL
		align 4
stru_1400067A8	UNWIND_INFO <0Ah, 4, 3,	0> ; DATA XREF:	.pdata:000000014000A2ACo
		UNWIND_CODE <1,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <4,	42h>	; UWOP_ALLOC_SMALL
		align 4
		dd rva __C_specific_handler
		dd 1
		C_SCOPE_TABLE <rva loc_140002F9C, rva loc_140002FAE, 1,	\
			       rva loc_140002FAE>
stru_1400067CC	UNWIND_INFO <1Ah, 13h, 3, 0> ; DATA XREF: .pdata:000000014000A264o
					; .pdata:000000014000A270o ...
		UNWIND_CODE <1,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <4,	82h>	; UWOP_ALLOC_SMALL
		align 4
		dd rva sub_140004B98
		dd 30h
stru_1400067E0	UNWIND_INFO <1Ah, 1Eh, 8, 0> ; DATA XREF: .pdata:000000014000A294o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Fh, 64h>	; UWOP_SAVE_NONVOL
		dw 0Dh
		UNWIND_CODE <0Fh, 34h>	; UWOP_SAVE_NONVOL
		dw 0Ch
		UNWIND_CODE <0Fh, 92h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
		dd rva sub_140004B98
		dd 40h
stru_1400067FC	UNWIND_INFO <2,	19h, 0Ch, 0> ; DATA XREF: .pdata:000000014000A504o
		UNWIND_CODE <3,	6>	; UWOP_EPILOG
		UNWIND_CODE <9Ch, 6>	; UWOP_EPILOG
		UNWIND_CODE <19h, 74h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <19h, 64h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <19h, 54h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <19h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <19h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <15h, 0E0h>	; UWOP_PUSH_NONVOL
stru_140006818	UNWIND_INFO <2,	0Dh, 6,	0> ; DATA XREF:	.pdata:000000014000A450o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Dh, 34h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <0Dh, 52h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	50h>	; UWOP_PUSH_NONVOL
stru_140006828	UNWIND_INFO <2,	0Fh, 8,	0> ; DATA XREF:	.pdata:000000014000A48Co
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Fh, 64h>	; UWOP_SAVE_NONVOL
		dw 0Bh
		UNWIND_CODE <0Fh, 34h>	; UWOP_SAVE_NONVOL
		dw 0Ah
		UNWIND_CODE <0Fh, 72h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
stru_14000683C	UNWIND_INFO <0Ah, 8, 6,	0> ; DATA XREF:	.pdata:000000014000A45Co
		UNWIND_CODE <4,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <8,	72h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <4,	70h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <3,	60h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <2,	30h>	; UWOP_PUSH_NONVOL
		dd rva __C_specific_handler
		dd 1
		C_SCOPE_TABLE <rva loc_14000B8DE, rva loc_14000B8E7, 1,	\
			       rva loc_14000B8E7>
stru_140006864	UNWIND_INFO <2,	1Bh, 0Ah, 0> ; DATA XREF: .pdata:000000014000A498o
		UNWIND_CODE <5,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <1Bh, 54h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <1Bh, 34h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <1Bh, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <17h, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <15h, 70h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <14h, 60h>	; UWOP_PUSH_NONVOL
stru_14000687C	UNWIND_INFO <1Ah, 27h, 0Dh, 25h> ; DATA	XREF: .pdata:000000014000A4B0o
		UNWIND_CODE <0Dh, 16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <19h, 23h>	; UWOP_SET_FPREG
		UNWIND_CODE <14h, 1>	; UWOP_ALLOC_LARGE
		dw 13h
		UNWIND_CODE <0Dh, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <0Bh, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <9,	0D0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <7,	0C0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <5,	70h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <4,	60h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <3,	30h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <2,	50h>	; UWOP_PUSH_NONVOL
		align 4
		dd rva sub_140004B98
		dd 80h
stru_1400068A4	UNWIND_INFO <2,	4, 3, 0> ; DATA	XREF: .pdata:000000014000A240o
					; .pdata:000000014000A384o ...
		UNWIND_CODE <1,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <4,	42h>	; UWOP_ALLOC_SMALL
		align 4
stru_1400068B0	UNWIND_INFO <2,	13h, 6,	0> ; DATA XREF:	.pdata:000000014000A468o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <13h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <13h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Fh, 70h>	; UWOP_PUSH_NONVOL
stru_1400068C0	UNWIND_INFO <2,	0Ah, 6,	0> ; DATA XREF:	.pdata:000000014000A2B8o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Ah, 34h>	; UWOP_SAVE_NONVOL
		dw 0Ch
		UNWIND_CODE <0Ah, 92h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
stru_1400068D0	UNWIND_INFO <2,	6, 4, 0> ; DATA	XREF: .pdata:000000014000A2C4o
					; .pdata:000000014000A3E4o ...
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <6,	32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <2,	30h>	; UWOP_PUSH_NONVOL
stru_1400068DC	UNWIND_INFO <2,	0Ah, 6,	0> ; DATA XREF:	.pdata:000000014000A330o
		UNWIND_CODE <2,	6>	; UWOP_EPILOG
		UNWIND_CODE <14h, 6>	; UWOP_EPILOG
		UNWIND_CODE <0Ah, 34h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <0Ah, 52h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
stru_1400068EC	UNWIND_INFO <2,	14h, 0Ah, 0> ; DATA XREF: .pdata:000000014000A2F4o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <14h, 64h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <14h, 54h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <14h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <14h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <10h, 70h>	; UWOP_PUSH_NONVOL
stru_140006904	UNWIND_INFO <2,	18h, 0Ch, 0> ; DATA XREF: .pdata:000000014000A318o
		UNWIND_CODE <6,	6>	; UWOP_EPILOG
		UNWIND_CODE <9,	16h>	; UWOP_EPILOG
		UNWIND_CODE <18h, 64h>	; UWOP_SAVE_NONVOL
		dw 0Ah
		UNWIND_CODE <18h, 54h>	; UWOP_SAVE_NONVOL
		dw 9
		UNWIND_CODE <18h, 34h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <18h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <14h, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <12h, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <10h, 70h>	; UWOP_PUSH_NONVOL
stru_140006920	UNWIND_INFO <1Ah, 22h, 0Ah, 0> ; DATA XREF: .pdata:000000014000A324o
		UNWIND_CODE <6,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <13h, 64h>	; UWOP_SAVE_NONVOL
		dw 11h
		UNWIND_CODE <13h, 34h>	; UWOP_SAVE_NONVOL
		dw 10h
		UNWIND_CODE <13h, 92h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Fh, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <0Dh, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
		dd rva sub_140004B98
		dd 40h
stru_140006940	UNWIND_INFO <1Ah, 0Ah, 6, 0> ; DATA XREF: .pdata:000000014000A354o
		UNWIND_CODE <2,	16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <0Ah, 34h>	; UWOP_SAVE_NONVOL
		dw 0Ah
		UNWIND_CODE <0Ah, 72h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
		dd rva __C_specific_handler
		dd 2
		C_SCOPE_TABLE <rva loc_1400049C1, rva loc_1400049D0, 1,	\
			       rva loc_140004A1F>
		C_SCOPE_TABLE <rva loc_14000499B, rva loc_140004A2E, \
			       rva sub_1400050DD, 0>
stru_140006978	UNWIND_INFO <2,	6, 4, 0> ; DATA	XREF: .pdata:000000014000A3CCo
		UNWIND_CODE <2,	6>	; UWOP_EPILOG
		UNWIND_CODE <3,	6>	; UWOP_EPILOG
		UNWIND_CODE <6,	52h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <2,	50h>	; UWOP_PUSH_NONVOL
stru_140006984	UNWIND_INFO <12h, 17h, 0Ch, 0> ; DATA XREF: .pdata:000000014000A360o
		UNWIND_CODE <0Ah, 16h>	; UWOP_EPILOG
		UNWIND_CODE <0,	6>	; UWOP_EPILOG
		UNWIND_CODE <17h, 64h>	; UWOP_SAVE_NONVOL
		dw 0Dh
		UNWIND_CODE <17h, 34h>	; UWOP_SAVE_NONVOL
		dw 0Ch
		UNWIND_CODE <17h, 52h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <13h, 0F0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <11h, 0E0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <0Fh, 0D0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <0Dh, 0C0h>	; UWOP_PUSH_NONVOL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
		dd rva __C_specific_handler
		dd 1
		C_SCOPE_TABLE <rva loc_140004A5E, rva loc_140004AFB, \
			       rva sub_1400050ED, 0>
stru_1400069B8	UNWIND_INFO <2,	6, 4, 0> ; DATA	XREF: .pdata:000000014000A3C0o
					; .pdata:000000014000A3D8o
		UNWIND_CODE <2,	6>	; UWOP_EPILOG
		UNWIND_CODE <3,	6>	; UWOP_EPILOG
		UNWIND_CODE <6,	32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <2,	50h>	; UWOP_PUSH_NONVOL
		align 8
stru_1400069C8	UNWIND_INFO <1,	0, 0, 0> ; DATA	XREF: .pdata:000000014000A36Co
stru_1400069CC	UNWIND_INFO <2,	4, 1, 0> ; DATA	XREF: .pdata:000000014000A378o
		UNWIND_CODE <4,	62h>	; UWOP_ALLOC_SMALL
		align 4
		align 8
stru_1400069D8	UNWIND_INFO <1,	0, 0, 0> ; DATA	XREF: .pdata:000000014000A3A8o
		align 20h
stru_1400069E0	UNWIND_INFO <1,	0, 0, 0> ; DATA	XREF: .pdata:000000014000A3B4o
stru_1400069E4	UNWIND_INFO <1,	4, 1, 0> ; DATA	XREF: .pdata:ExceptionDiro
					; .pdata:000000014000A00Co
		UNWIND_CODE <4,	42h>	; UWOP_ALLOC_SMALL
		align 4
stru_1400069EC	UNWIND_INFO <1,	14h, 8,	0> ; DATA XREF:	.pdata:000000014000A018o
		UNWIND_CODE <14h, 64h>	; UWOP_SAVE_NONVOL
		dw 8
		UNWIND_CODE <14h, 54h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <14h, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <14h, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <10h, 70h>	; UWOP_PUSH_NONVOL
stru_140006A00	UNWIND_INFO <1,	0Ah, 4,	0> ; DATA XREF:	.pdata:000000014000A024o
					; .pdata:000000014000A030o ...
		UNWIND_CODE <0Ah, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Ah, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <6,	70h>	; UWOP_PUSH_NONVOL
stru_140006A0C	UNWIND_INFO <1,	0Fh, 6,	0> ; DATA XREF:	.pdata:000000014000A03Co
		UNWIND_CODE <0Fh, 64h>	; UWOP_SAVE_NONVOL
		dw 7
		UNWIND_CODE <0Fh, 34h>	; UWOP_SAVE_NONVOL
		dw 6
		UNWIND_CODE <0Fh, 32h>	; UWOP_ALLOC_SMALL
		UNWIND_CODE <0Bh, 70h>	; UWOP_PUSH_NONVOL
		align 20h
stru_140006A20	UNWIND_INFO <1,	0, 0, 0> ; DATA	XREF: .pdata:000000014000A39Co
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_rdata		ends

; Section 3. (virtual address 00007000)
; Virtual size			: 00002B68 (  11112.)
; Section size in file		: 00000200 (	512.)
; Offset to raw	data for section: 00005200
; Flags	C8000040: Data Not pageable Readable Writable
; Alignment	: default
; ===========================================================================

; Segment type:	Pure data
; Segment permissions: Read/Write
_data		segment	para public 'DATA' use64
		assume cs:_data
		;org 140007000h
qword_140007000	dq 0FFFFF6FB7DBED000h	; DATA XREF: set_func_and_page_table_pointers:loc_14000D270r
qword_140007008	dq 0FFFFF6FB7DA00000h	; DATA XREF: set_func_and_page_table_pointers+104r
qword_140007010	dq 0FFFFF6FB40000000h	; DATA XREF: set_func_and_page_table_pointers+112r
qword_140007018	dq 0FFFFF68000000000h	; DATA XREF: set_func_and_page_table_pointers+120r
; ULONG_PTR _security_cookie
__security_cookie dq 2B992DDFA232h	; DATA XREF: sub_140002D30+4r
					; sub_140002D70+4r ...
; ULONG_PTR BugCheckParameter3
BugCheckParameter3 dq 0FFFFD466D2205DCDh ; DATA	XREF: sub_140004B50+2Dr
					; cookie_func1+59w
wdf_version	db  30h	; 0		; DATA XREF: unbind_stuff+4o
					; unbind_stuff+17o ...
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		dq offset aKmdflibrary	; "KmdfLibrary"
		db    1
		db    0
		db    0
		db    0
		db    9
		db    0
		db    0
		db    0
		db 0B0h	; ∞
		db  1Dh
		db    0
		db    0
		db  8Ch	; å
		db    1
		db    0
		db    0
		dq offset unk_140008CC0
		align 20h
unk_140007060	db    0			; DATA XREF: sub_1400011B0+14o
					; .data:off_140007078o
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
unk_140007070	db    0			; DATA XREF: sub_1400011B0+1Bo
					; maybe_useless+14o ...
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
off_140007078	dq offset unk_140007060	; DATA XREF: sub_1400011B0+Ar
					; sub_1400011B0+63r ...
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
unk_140007090	db    0			; DATA XREF: maybe_useless_v2+Ao
					; maybe_useless_v2+11o
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
unk_1400070A0	db    0			; DATA XREF: sub_14000B000+7o
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
unk_1400070B0	db    0			; DATA XREF: maybe_useless_v2+2Ao
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    0
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
dword_1400072E0	dd ?			; DATA XREF: sub_14000B000w
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
dword_140007308	dd ?			; DATA XREF: main_run_stuff:loc_14000D054w
dword_14000730C	dd ?			; DATA XREF: main_run_stuff+5Ew
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
unk_140007330	db    ?	;		; DATA XREF: sub_140002BBC+7o
					; sub_14000B330+4Bo
unk_140007331	db    ?	;		; DATA XREF: sub_14000B330+89o
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
byte_140008C20	db ?			; DATA XREF: sub_140002BBC+6Ao
					; sub_140002BBC:loc_140002C43r	...
		align 8
some_linked_list dq ?			; DATA XREF: empty_linked_list_and_call_cb:loc_14000B5F2r
					; empty_linked_list_and_call_cb+19w
qword_140008C30	dq ?			; DATA XREF: set_func_and_page_table_pointers+19Cw
qword_140008C38	dq ?			; DATA XREF: sub_140002FE4+12r
					; set_func_and_page_table_pointers+1A3w
; PVOID	P
P		dq ?			; DATA XREF: sub_140002D28r
					; sub_14000B71C+4r ...
; int (__fastcall *nm_allocate_contiguous_node_mem)(_QWORD, _QWORD, _QWORD, _QWORD)
nm_allocate_contiguous_node_mem	dq ?	; DATA XREF: INIT_HOST_RSP+4r
					; set_func_and_page_table_pointers+1C1w
page_table_ptr1	dq ?			; DATA XREF: set_func_and_page_table_pointers+E0w
					; set_func_and_page_table_pointers+FDw
page_table_ptr2	dq ?			; DATA XREF: set_func_and_page_table_pointers+D9w
					; set_func_and_page_table_pointers+10Bw
page_table_ptr3	dq ?			; DATA XREF: sub_140002E3C+40r
					; set_func_and_page_table_pointers+E7w	...
page_table_ptr4	dq ?			; DATA XREF: set_func_and_page_table_pointers+B0w
					; set_func_and_page_table_pointers+127w
qword_140008C70	dq ?			; DATA XREF: set_func_and_page_table_pointers+17Fw
qword_140008C78	dq ?			; DATA XREF: set_func_and_page_table_pointers+174w
qword_140008C80	dq ?			; DATA XREF: set_func_and_page_table_pointers+157w
qword_140008C88	dq ?			; DATA XREF: set_func_and_page_table_pointers+14Cw
qword_140008C90	dq ?			; DATA XREF: set_func_and_page_table_pointers+16Dw
qword_140008C98	dq ?			; DATA XREF: set_func_and_page_table_pointers+162w
qword_140008CA0	dq ?			; DATA XREF: set_func_and_page_table_pointers+138w
main_page_table	dq ?			; DATA XREF: set_func_and_page_table_pointers+143w
do_some_xor_decode dd ?			; DATA XREF: xordecw
		align 8
; PMDL MemoryDescriptorList
MemoryDescriptorList dq	?		; DATA XREF: VMCALL_HANDLER+A77r
					; VMCALL_HANDLER+A90w ...
unk_140008CC0	db    ?	;		; DATA XREF: .data:0000000140007050o
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
unk_140009308	db    ?	;		; DATA XREF: drivermain+E6r
					; drivermain+FBw
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
; UNICODE_STRING unk_140009928
unk_140009928	db    ?	;		; DATA XREF: unbind_stuff+1Eo
					; drivermain+39o ...
		db    ?	;
unk_14000992A	db    ?	;		; DATA XREF: drivermain+40w
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
unk_140009930	db    ?	;		; DATA XREF: drivermain+55w
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
; int (*unk_140009938)(void)
unk_140009938	db    ?	;		; DATA XREF: driver_unload_func+4r
					; drivermain+BCr ...
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
unk_140009940	db    ?	;		; DATA XREF: drivermain+EDw
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
wdf_globals	db    ?	;		; DATA XREF: unbind_stuff+10r
					; drivermain+62o ...
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
unk_140009950	db    ?	;		; DATA XREF: drivermain+32w
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
unk_140009960	db    ?	;		; DATA XREF: drivermain+47o
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
		db    ?	;
_data		ends

; Section 4. (virtual address 0000A000)
; Virtual size			: 00000510 (   1296.)
; Section size in file		: 00000600 (   1536.)
; Offset to raw	data for section: 00005400
; Flags	48000040: Data Not pageable Readable
; Alignment	: default
; ===========================================================================

; Segment type:	Pure data
; Segment permissions: Read
_pdata		segment	para public 'DATA' use64
		assume cs:_pdata
		;org 14000A000h
ExceptionDir	RUNTIME_FUNCTION <rva unbind_stuff, rva	algn_14000102E,	\
				  rva stru_1400069E4>
		RUNTIME_FUNCTION <rva driver_unload_func, rva algn_14000105F, \
				  rva stru_1400069E4>
		RUNTIME_FUNCTION <rva drivermain, rva algn_140001182, \
				  rva stru_1400069EC>
		RUNTIME_FUNCTION <rva DriverEntry, rva algn_1400011AE, \
				  rva stru_140006A00>
		RUNTIME_FUNCTION <rva sub_1400011B0, rva algn_140001227, \
				  rva stru_140006A00>
		RUNTIME_FUNCTION <rva maybe_useless, rva algn_1400012AD, \
				  rva stru_140006A0C>
		RUNTIME_FUNCTION <rva maybe_useless_v2,	rva algn_140001314, \
				  rva stru_140006A00>
		RUNTIME_FUNCTION <rva sub_1400016EC, rva algn_140001741, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_140001744, rva algn_14000177F, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001780, rva algn_1400017C5, \
				  rva stru_1400065D8>
		RUNTIME_FUNCTION <rva sub_1400017C8, rva algn_140001815, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001818, rva algn_14000187D, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_140001900, rva sub_140001944,	\
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001944, rva algn_14000198B, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_14000198C, rva sub_140001A08,	\
				  rva stru_140006590>
		RUNTIME_FUNCTION <rva sub_140001A08, rva algn_140001A8A, \
				  rva stru_140006590>
		RUNTIME_FUNCTION <rva sub_140001A8C, rva algn_140001B1F, \
				  rva stru_1400065A8>
		RUNTIME_FUNCTION <rva sub_140001B48, rva sub_140001B90,	\
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001B90, rva algn_140001BE3, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_140001BE4, rva algn_140001C39, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_140001C3C, rva algn_140001C77, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001C78, rva algn_140001CB5, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001CB8, rva algn_140001D71, \
				  rva stru_140006600>
		RUNTIME_FUNCTION <rva sub_140001D74, rva algn_140001E01, \
				  rva stru_1400065E4>
		RUNTIME_FUNCTION <rva sub_140001E04, rva algn_140001EB9, \
				  rva stru_140006600>
		RUNTIME_FUNCTION <rva sub_140001EBC, rva algn_140001F17, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001F18, rva algn_140001F73, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140001F74, rva algn_140001FAA, \
				  rva stru_1400065D8>
		RUNTIME_FUNCTION <rva sub_140001FAC, rva sub_140001FE0,	\
				  rva stru_1400065D8>
		RUNTIME_FUNCTION <rva sub_140001FE0, rva algn_14000201B, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_14000201C, rva algn_140002057, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140002084, rva algn_1400020CB, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_1400020CC, rva sub_140002114,	\
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140002114, rva sub_14000216C,	\
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_140002198, rva algn_140002209, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_14000220C, rva algn_14000227B, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_14000227C, rva algn_1400022C3, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_1400022C4, rva algn_1400022FF, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva sub_140002300, rva algn_140002353, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_140002354, rva algn_1400023A9, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_1400023AC, rva sub_1400026A8,	\
				  rva stru_140006558>
		RUNTIME_FUNCTION <rva sub_1400026C4, rva algn_1400027C3, \
				  rva stru_140006770>
		RUNTIME_FUNCTION <rva sub_1400027C4, rva algn_140002809, \
				  rva stru_1400066A4>
		RUNTIME_FUNCTION <rva sub_14000280C, rva algn_14000286E, \
				  rva stru_1400066E4>
		RUNTIME_FUNCTION <rva sub_140002870, rva algn_1400029E2, \
				  rva stru_1400066B0>
		RUNTIME_FUNCTION <rva sub_1400029E4, rva sub_140002A84,	\
				  rva stru_1400066CC>
		RUNTIME_FUNCTION <rva sub_140002A84, rva algn_140002ADE, \
				  rva stru_140006720>
		RUNTIME_FUNCTION <rva sub_140002AE0, rva sub_140002BBC,	\ ; rcx	: weird	initialized stuff
				  rva stru_140006708> ;
		RUNTIME_FUNCTION <rva sub_140002BBC, rva sub_140002C58,	\
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva sub_140002C58, rva algn_140002CDB, \
				  rva stru_1400066F4>
		RUNTIME_FUNCTION <rva INIT_HOST_RSP, rva algn_140002D1E, \
				  rva stru_140006798>
		RUNTIME_FUNCTION <rva sub_140002D30, rva algn_140002D6E, \
				  rva stru_1400067CC>
		RUNTIME_FUNCTION <rva sub_140002D70, rva algn_140002DAE, \
				  rva stru_1400067CC>
		RUNTIME_FUNCTION <rva invpid_wrap, rva algn_140002DF2, \
				  rva stru_1400067CC>
		RUNTIME_FUNCTION <rva sub_140002DF4, rva algn_140002E37, \
				  rva stru_1400067CC>
		RUNTIME_FUNCTION <rva sub_140002E3C, rva algn_140002EF6, \
				  rva stru_1400067E0>
		RUNTIME_FUNCTION <rva find_substring_pos, rva algn_140002F6E, \	; (target_area,	target_len, pattern, pattern_len
				  rva stru_140006770>
		RUNTIME_FUNCTION <rva vm_call_wrapper, rva do_vm_read, \
				  rva stru_1400067A8>
		RUNTIME_FUNCTION <rva VM_ENTRY_HANDLER,	rva algn_1400030B6, \
				  rva stru_1400068C0>
		RUNTIME_FUNCTION <rva sub_1400030B8, rva sub_1400030E4,	\
				  rva stru_1400068D0>
		RUNTIME_FUNCTION <rva sub_1400030E4, rva algn_140003143, \
				  rva stru_1400066E4>
		RUNTIME_FUNCTION <rva sub_140003144, rva algn_1400032F2, \
				  rva stru_1400065C4>
		RUNTIME_FUNCTION <rva sub_1400032F4, rva algn_1400033A6, \
				  rva stru_140006580>
		RUNTIME_FUNCTION <rva handle_exit_intr,	rva algn_14000347B, \
				  rva stru_1400068EC>
		RUNTIME_FUNCTION <rva sub_14000347C, rva algn_140003633, \
				  rva stru_1400065E4>
		RUNTIME_FUNCTION <rva sub_140003634, rva algn_1400037FE, \
				  rva stru_1400065E4>
		RUNTIME_FUNCTION <rva VMCALL_HANDLER, rva algn_14000443D, \ ; rdx=0x12
				  rva stru_140006904> ;	rcx=ptr	to host	rsp
		RUNTIME_FUNCTION <rva sub_140004440, rva algn_140004527, \
				  rva stru_140006920>
		RUNTIME_FUNCTION <rva real_handler, rva	unk_1400047E9, \
				  rva stru_1400068DC>
		RUNTIME_FUNCTION <rva set_rflags, rva algn_14000481B, \
				  rva stru_1400065D8>
		RUNTIME_FUNCTION <rva set_intr_data, rva algn_140004876, \
				  rva stru_1400066E4>
		RUNTIME_FUNCTION <rva allocate_stuff, rva algn_140004A3B, \
				  rva stru_140006940>
		RUNTIME_FUNCTION <rva do_something_to_text_seg,	rva algn_140004B15, \
				  rva stru_140006984>
		RUNTIME_FUNCTION <rva sub_140004B50, rva algn_140004B6E, \
				  rva stru_1400069C8>
		RUNTIME_FUNCTION <rva loc_140004B70, rva algn_140004B96+1, \
				  rva stru_1400069CC>
		RUNTIME_FUNCTION <rva sub_140004B98, rva algn_140004BB5, \
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva sub_140004BB8, rva algn_140004C17, \
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva sub_140004C60, rva algn_140004C62, \
				  rva stru_140006A20>
		RUNTIME_FUNCTION <rva init_memory, rva algn_140004D79, \
				  rva stru_1400069D8>
		RUNTIME_FUNCTION <rva sub_140004D80, rva algn_1400050B9, \
				  rva stru_1400069E0>
		RUNTIME_FUNCTION <rva sub_1400050C6, rva sub_1400050DD,	\
				  rva stru_1400069B8>
		RUNTIME_FUNCTION <rva sub_1400050DD, rva sub_1400050ED,	\
				  rva stru_140006978>
		RUNTIME_FUNCTION <rva sub_1400050ED, rva algn_1400050FC+1, \
				  rva stru_1400069B8>
		RUNTIME_FUNCTION <rva loc_14000B014, rva new_unload_func, \
				  rva stru_1400068D0>
		RUNTIME_FUNCTION <rva new_unload_func, rva algn_14000B0DB, \
				  rva stru_14000663C>
		RUNTIME_FUNCTION <rva init_CSTRUCT_0x20, rva algn_14000B32E, \
				  rva stru_140006684>
		RUNTIME_FUNCTION <rva sub_14000B330, rva algn_14000B5A2, \
				  rva stru_14000665C>
		RUNTIME_FUNCTION <rva sub_14000B5A4, rva algn_14000B5EA, \
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva empty_linked_list_and_call_cb, \ ; arg0 =	init_s0_data()
				  rva execute_func_on_each_proc, rva stru_1400068D0>
		RUNTIME_FUNCTION <rva execute_func_on_each_proc, rva algn_14000B6E9, \ ; arg0 =	init_s0_data()
				  rva stru_140006750>
		RUNTIME_FUNCTION <rva get_routine_address, rva algn_14000B71A, \
				  rva stru_14000678C>
		RUNTIME_FUNCTION <rva sub_14000B71C, rva sub_14000B73C,	\
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva sub_14000B73C, rva algn_14000B81A, \
				  rva stru_140006818>
		RUNTIME_FUNCTION <rva sub_14000B82C, rva algn_14000B94D, \
				  rva stru_14000683C>
		RUNTIME_FUNCTION <rva sub_14000B950, rva algn_14000BA06, \
				  rva stru_1400068B0>
		RUNTIME_FUNCTION <rva sub_14000BA08, rva algn_14000BA2F, \
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva sub_14000BA30, rva algn_14000BA8B, \
				  rva stru_1400066E4>
		RUNTIME_FUNCTION <rva init_s0_data, rva	algn_14000BBCA,	\
				  rva stru_140006828>
		RUNTIME_FUNCTION <rva gogolaunch, rva wmsr_stuff, rva stru_140006864> ;	r8 = init_s0_data
					; rdx =	some_args1
		RUNTIME_FUNCTION <rva wmsr_stuff, rva algn_14000BE2D, \
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva sub_14000BE30, rva algn_14000C613, \ ; r8=some_args1
				  rva stru_14000687C>
		RUNTIME_FUNCTION <rva gogolaunch_wrap, rva algn_14000C637, \
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva sub_14000C638, rva algn_14000C67C, \
				  rva stru_1400068A4>
		RUNTIME_FUNCTION <rva main_run_stuff, rva algn_14000D0E2, \
				  rva stru_140006620>
		RUNTIME_FUNCTION <rva more_version_check, rva algn_14000D149, \
				  rva stru_140006648>
		RUNTIME_FUNCTION <rva no_cb_called, rva	algn_14000D17E,	\
				  rva stru_1400066E4>
		RUNTIME_FUNCTION <rva set_func_and_page_table_pointers,	\
				  rva algn_14000D36B, rva stru_140006734>
		RUNTIME_FUNCTION <rva sub_14000D36C, rva algn_14000D499, \
				  rva stru_1400067FC>
		align 1000h
_pdata		ends

; Section 5. (virtual address 0000B000)
; Virtual size			: 0000167C (   5756.)
; Section size in file		: 00001800 (   6144.)
; Offset to raw	data for section: 00005A00
; Flags	60000020: Text Executable Readable
; Alignment	: default
; ===========================================================================

; Segment type:	Pure code
; Segment permissions: Read/Execute
PAGE		segment	para public 'CODE' use64
		assume cs:PAGE
		;org 14000B000h
		assume es:nothing, ss:nothing, ds:_data, fs:nothing, gs:nothing

; =============== S U B	R O U T	I N E =======================================


sub_14000B000	proc near		; CODE XREF: main_run_stuff+94p
		and	cs:dword_1400072E0, 0
		lea	rcx, unk_1400070A0
		jmp	loc_14000B014
; ---------------------------------------------------------------------------
		align 4

loc_14000B014:				; CODE XREF: sub_14000B000+Ej
					; DATA XREF: .pdata:000000014000A3E4o
		push	rbx
		sub	rsp, 20h
		cmp	qword ptr [rcx+0A8h], 0
		mov	rbx, rcx
		jz	short loc_14000B05E
		mov	byte ptr [rcx+0A1h], 0
		xor	r8d, r8d

some_object:
		mov	rcx, [rcx+0A8h]
		xor	edx, edx
		call	cs:ZwWaitForSingleObject
		test	eax, eax
		jns	short loc_14000B049
		call	sub_140001588

loc_14000B049:				; CODE XREF: sub_14000B000+42j
		mov	rcx, [rbx+0A8h]	; Handle
		call	cs:ZwClose
		and	qword ptr [rbx+0A8h], 0

loc_14000B05E:				; CODE XREF: sub_14000B000+25j
		mov	rcx, [rbx+28h]	; Handle
		test	rcx, rcx
		jz	short loc_14000B072
		call	cs:ZwClose
		and	qword ptr [rbx+28h], 0

loc_14000B072:				; CODE XREF: sub_14000B000+65j
		mov	rcx, [rbx+18h]	; P
		test	rcx, rcx
		jz	short loc_14000B08B
		mov	edx, 20676F6Ch	; Tag
		call	cs:ExFreePoolWithTag
		and	qword ptr [rbx+18h], 0

loc_14000B08B:				; CODE XREF: sub_14000B000+79j
		mov	rcx, [rbx+10h]	; P
		test	rcx, rcx
		jz	short loc_14000B0A4
		mov	edx, 20676F6Ch	; Tag
		call	cs:ExFreePoolWithTag
		and	qword ptr [rbx+10h], 0

loc_14000B0A4:				; CODE XREF: sub_14000B000+92j
		cmp	byte ptr [rbx+0A0h], 0
		jz	short loc_14000B0BE
		lea	rcx, [rbx+38h]	; Resource
		call	cs:ExDeleteResourceLite
		mov	byte ptr [rbx+0A0h], 0

loc_14000B0BE:				; CODE XREF: sub_14000B000+ABj
		add	rsp, 20h
		pop	rbx
		retn
sub_14000B000	endp


; =============== S U B	R O U T	I N E =======================================


new_unload_func	proc near		; DATA XREF: .pdata:000000014000A3E4o
					; .pdata:000000014000A3F0o ...
		sub	rsp, 28h
		call	sub_14000B81C
		call	sub_14000B71C
		add	rsp, 28h
		jmp	empty_linked_list_and_call_cb
new_unload_func	endp

; ---------------------------------------------------------------------------
algn_14000B0DB:				; DATA XREF: .pdata:000000014000A3F0o
		align 4

; =============== S U B	R O U T	I N E =======================================


init_CSTRUCT_0x20 proc near		; CODE XREF: gogolaunch+5Ap
					; DATA XREF: .pdata:000000014000A3FCo

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		mov	[rsp+arg_10], rsi
		push	rdi
		push	r12
		push	r13
		push	r14
		push	r15
		sub	rsp, 20h
		mov	r13d, 56484C46h
		mov	edi, 20h
		mov	r8d, r13d	; Tag
		mov	edx, edi	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	rbx, rax
		test	rax, rax
		jz	loc_14000B30F
		mov	r8d, edi
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		mov	ebp, 1000h
		mov	r8d, r13d	; Tag
		mov	edx, ebp	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	rdi, rax
		test	rax, rax
		jz	loc_14000B303
		mov	r8d, ebp
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		mov	r8d, r13d	; Tag
		mov	edx, ebp	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	rsi, rax
		test	rax, rax
		jz	loc_14000B2F7
		mov	r8d, ebp
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		mov	rcx, rsi
		call	MmGetPhysicalAddress
		mov	rcx, rax
		call	sub_140002BBC
		movzx	r10d, al
		mov	rcx, rsi
		mov	rax, [rdi]
		and	r10d, 7
		and	rax, 0FFFFFFFFFFFFFFD8h
		or	r10, rax
		or	r10, 18h
		mov	[rdi], r10
		call	MmGetPhysicalAddress
		mov	rcx, rax
		call	sub_140002F78
		shl	rax, 0Ch
		mov	rcx, 0FFFFFFFFF000h
		xor	rax, [rdi]
		and	rax, rcx
		xor	[rdi], rax
		call	sub_140002D28
		xor	r15d, r15d
		mov	r12, rax
		cmp	[rax], r15d
		jbe	short loc_14000B22B

loc_14000B1DA:				; CODE XREF: init_CSTRUCT_0x20+147j
		mov	r14d, r15d
		xor	ebp, ebp
		inc	r14
		add	r14, r14
		mov	r13, [r12+r14*8]
		cmp	[r12+r14*8+8], rbp
		jbe	short loc_14000B21C

loc_14000B1F0:				; CODE XREF: init_CSTRUCT_0x20+13Ej
		xor	r9d, r9d
		mov	r8, rbp
		add	r8, r13
		mov	rcx, rsi
		shl	r8, 0Ch
		lea	edx, [r9+4]
		call	sub_140002870
		test	rax, rax
		jz	loc_14000B2BF
		inc	rbp
		cmp	rbp, [r12+r14*8+8]
		jb	short loc_14000B1F0

loc_14000B21C:				; CODE XREF: init_CSTRUCT_0x20+112j
		inc	r15d
		cmp	r15d, [r12]
		jb	short loc_14000B1DA
		mov	r13d, 56484C46h

loc_14000B22B:				; CODE XREF: init_CSTRUCT_0x20+FCj
		mov	ecx, 1Bh
		call	read_some_msr
		shr	rax, 0Ch
		xor	r9d, r9d
		and	eax, 0FFFFFFh
		mov	rcx, rsi
		shl	rax, 0Ch
		mov	r8, rax
		lea	edx, [r9+4]
		call	sub_140002870
		test	rax, rax
		jz	loc_14000B2EA
		mov	r14d, 190h
		mov	r8d, r13d	; Tag
		mov	edx, r14d	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	rbp, rax
		test	rax, rax
		jz	short loc_14000B2EA
		mov	r8d, r14d
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		xor	r14d, r14d
		mov	r15, rbp

loc_14000B28C:				; CODE XREF: init_CSTRUCT_0x20+1CAj
		xor	ecx, ecx
		call	sub_14000280C
		test	rax, rax
		jz	short loc_14000B2E0
		mov	[r15], rax
		inc	r14d
		add	r15, 8
		cmp	r14d, 32h
		jb	short loc_14000B28C
		mov	[rbx], rdi
		mov	rax, rbx
		mov	[rbx+8], rsi
		mov	[rbx+10h], rbp
		mov	dword ptr [rbx+18h], 0
		jmp	short loc_14000B311
; ---------------------------------------------------------------------------

loc_14000B2BF:				; CODE XREF: init_CSTRUCT_0x20+130j
		mov	edx, 4
		mov	rcx, rsi
		call	sub_1400029E4
		mov	esi, 56484C46h
		mov	rcx, rdi	; P
		mov	edx, esi	; Tag
		call	cs:ExFreePoolWithTag
		mov	edx, esi
		jmp	short loc_14000B306
; ---------------------------------------------------------------------------

loc_14000B2E0:				; CODE XREF: init_CSTRUCT_0x20+1BAj
		xor	edx, edx
		mov	rcx, rbp
		call	sub_140002A84

loc_14000B2EA:				; CODE XREF: init_CSTRUCT_0x20+17Bj
					; init_CSTRUCT_0x20+19Bj
		mov	edx, 4
		mov	rcx, rsi
		call	sub_1400029E4

loc_14000B2F7:				; CODE XREF: init_CSTRUCT_0x20+8Bj
		mov	edx, r13d	; Tag
		mov	rcx, rdi	; P
		call	cs:ExFreePoolWithTag

loc_14000B303:				; CODE XREF: init_CSTRUCT_0x20+65j
		mov	edx, r13d	; Tag

loc_14000B306:				; CODE XREF: init_CSTRUCT_0x20+202j
		mov	rcx, rbx	; P
		call	cs:ExFreePoolWithTag

loc_14000B30F:				; CODE XREF: init_CSTRUCT_0x20+3Aj
		xor	eax, eax

loc_14000B311:				; CODE XREF: init_CSTRUCT_0x20+1E1j
		mov	rbx, [rsp+48h+arg_0]
		mov	rbp, [rsp+48h+arg_8]
		mov	rsi, [rsp+48h+arg_10]
		add	rsp, 20h
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	rdi
		retn
init_CSTRUCT_0x20 endp

; ---------------------------------------------------------------------------
algn_14000B32E:				; DATA XREF: .pdata:000000014000A3FCo
		align 10h

; =============== S U B	R O U T	I N E =======================================


sub_14000B330	proc near		; CODE XREF: sub_14000B73C:loc_14000B7DEp
					; DATA XREF: .pdata:000000014000A408o

var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r13
		push	r14
		push	r15
		sub	rsp, 30h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+48h+var_20], rax
		mov	ecx, 2FFh
		xor	esi, esi
		call	read_some_msr
		mov	rbx, rax
		mov	ecx, 0FEh
		mov	cs:byte_140008C20, bl
		call	read_some_msr
		lea	r13, unk_140007330
		mov	rdi, rax
		bt	rax, 8
		jnb	loc_14000B4E4
		bt	rbx, 0Ah
		jnb	loc_14000B4E4
		mov	ecx, 250h
		xor	ebp, ebp
		call	read_some_msr
		mov	[rsp+48h+var_28], rax
		lea	rcx, [rsp+48h+var_20]
		lea	rax, [rsp+48h+var_28]
		cmp	rcx, rax
		lea	rdx, unk_140007331
		sbb	rbx, rbx
		not	rbx
		and	ebx, 8
		xor	r8d, r8d

loc_14000B3CC:				; CODE XREF: sub_14000B330+CFj
		mov	al, byte ptr [rsp+r8+48h+var_28]
		mov	rcx, rbp
		mov	[rdx+1], al
		add	rbp, 10000h
		mov	word ptr [rdx-1], 101h
		inc	esi
		mov	[rdx+7], rcx
		lea	rdx, [rdx+18h]
		lea	rax, [rcx+0FFFFh]
		inc	r8
		mov	[rdx-9], rax
		cmp	r8, rbx
		jnz	short loc_14000B3CC
		xor	r15d, r15d
		movsxd	r14, esi
		mov	ebp, 258h

loc_14000B40C:				; CODE XREF: sub_14000B330+13Bj
		mov	ecx, ebp
		call	read_some_msr
		mov	[rsp+48h+var_28], rax
		lea	rdx, [r13+1]
		lea	rax, [r14+r14*2]
		xor	r8d, r8d
		lea	rdx, [rdx+rax*8]

loc_14000B427:				; CODE XREF: sub_14000B330+131j
		mov	al, byte ptr [rsp+r8+48h+var_28]
		lea	rcx, [r15+80000h]
		mov	[rdx+1], al
		lea	rax, [rcx+3FFFh]
		mov	[rdx+0Fh], rax
		add	r15, 4000h
		mov	word ptr [rdx-1], 101h
		inc	esi
		mov	[rdx+7], rcx
		lea	rdx, [rdx+18h]
		inc	r14
		inc	r8
		cmp	r8, rbx
		jnz	short loc_14000B427
		inc	ebp
		cmp	ebp, 259h
		jbe	short loc_14000B40C
		xor	ebp, ebp
		movsxd	r14, esi
		mov	ebx, 268h

loc_14000B477:				; CODE XREF: sub_14000B330+1B2j
		mov	ecx, ebx
		call	read_some_msr
		mov	[rsp+48h+var_28], rax
		lea	rdx, [r13+1]
		lea	rax, [r14+r14*2]
		lea	rdx, [rdx+rax*8]
		lea	r8, [rsp+48h+var_28]

loc_14000B494:				; CODE XREF: sub_14000B330+1A8j
		mov	al, [r8]
		lea	rcx, [rbp+0C0000h]
		mov	[rdx+1], al
		lea	rax, [rcx+0FFFh]
		mov	[rdx+0Fh], rax
		inc	r8
		mov	[rdx+7], rcx
		mov	rax, r8
		mov	word ptr [rdx-1], 101h
		lea	rdx, [rdx+18h]
		lea	rcx, [rsp+48h+var_28]
		add	rbp, 1000h
		sub	rax, rcx
		inc	esi
		inc	r14
		cmp	rax, 8
		jnz	short loc_14000B494
		inc	ebx
		cmp	ebx, 26Fh
		jbe	short loc_14000B477

loc_14000B4E4:				; CODE XREF: sub_14000B330+5Aj
					; sub_14000B330+65j
		xor	ebp, ebp
		movzx	r14d, dil
		test	dil, dil
		jz	loc_14000B576
		movsxd	rax, esi
		mov	edi, 200h
		lea	rsi, [r13+1]
		mov	r15, 0FFFFFFFFFh
		lea	rcx, [rax+rax*2]
		lea	rsi, [rsi+rcx*8]

loc_14000B511:				; CODE XREF: sub_14000B330+244j
		lea	ecx, [rdi+1]
		call	read_some_msr
		bt	rax, 0Bh
		jnb	short loc_14000B569
		shr	rax, 0Ch
		mov	ecx, edi
		and	rax, r15
		shl	rax, 0Ch
		bsf	rbx, rax
		call	read_some_msr
		mov	rdx, rax
		mov	[rsi+1], al
		shr	rdx, 0Ch
		mov	ecx, ebx
		and	rdx, r15
		mov	word ptr [rsi-1], 1
		shl	rdx, 0Ch
		mov	eax, 1
		shl	rax, cl
		dec	rax
		mov	[rsi+7], rdx
		add	rax, rdx
		mov	[rsi+0Fh], rax
		add	rsi, 18h

loc_14000B569:				; CODE XREF: sub_14000B330+1EEj
		inc	ebp
		add	edi, 2
		movsxd	rax, ebp
		cmp	rax, r14
		jb	short loc_14000B511

loc_14000B576:				; CODE XREF: sub_14000B330+1BDj
		mov	rcx, [rsp+48h+var_20]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		mov	rbx, [rsp+48h+arg_0]
		mov	rbp, [rsp+48h+arg_8]
		mov	rsi, [rsp+48h+arg_10]
		mov	rdi, [rsp+48h+arg_18]
		add	rsp, 30h
		pop	r15
		pop	r14
		pop	r13
		retn
sub_14000B330	endp

; ---------------------------------------------------------------------------
algn_14000B5A2:				; DATA XREF: .pdata:000000014000A408o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000B5A4	proc near		; CODE XREF: sub_14000B73C+85p
					; DATA XREF: .pdata:000000014000A414o
		sub	rsp, 28h
		mov	ecx, 48Ch
		call	read_some_msr
		mov	edx, 6104040h
		mov	ecx, eax
		and	ecx, edx
		cmp	ecx, edx
		jnz	short loc_14000B5E3
		shr	rax, 20h
		test	al, 1
		jz	short loc_14000B5E3
		bt	eax, 8
		jnb	short loc_14000B5E3
		bt	eax, 9
		jnb	short loc_14000B5E3
		bt	eax, 0Ah
		jnb	short loc_14000B5E3
		bt	eax, 0Bh
		jnb	short loc_14000B5E3
		mov	al, 1
		jmp	short loc_14000B5E5
; ---------------------------------------------------------------------------

loc_14000B5E3:				; CODE XREF: sub_14000B5A4+19j
					; sub_14000B5A4+21j ...
		xor	al, al

loc_14000B5E5:				; CODE XREF: sub_14000B5A4+3Dj
		add	rsp, 28h
		retn
sub_14000B5A4	endp

; ---------------------------------------------------------------------------
algn_14000B5EA:				; DATA XREF: .pdata:000000014000A414o
		align 4

; =============== S U B	R O U T	I N E =======================================


empty_linked_list_and_call_cb proc near	; CODE XREF: new_unload_func+12j
					; main_run_stuff+8Fp ...
		push	rbx
		sub	rsp, 20h

loc_14000B5F2:				; CODE XREF: empty_linked_list_and_call_cb+30j
		mov	rcx, cs:some_linked_list
		test	rcx, rcx
		jz	short loc_14000B61E
		mov	rax, [rcx]
		lea	rbx, [rcx-8]
		mov	cs:some_linked_list, rax
		call	qword ptr [rbx]
		mov	edx, 6A624F47h	; Tag
		mov	rcx, rbx	; P
		call	cs:ExFreePoolWithTag
		jmp	short loc_14000B5F2
; ---------------------------------------------------------------------------

loc_14000B61E:				; CODE XREF: empty_linked_list_and_call_cb+10j
		add	rsp, 20h
		pop	rbx
		retn
empty_linked_list_and_call_cb endp


; =============== S U B	R O U T	I N E =======================================

; arg0 = init_s0_data()
; Attributes: bp-based frame

execute_func_on_each_proc proc near	; CODE XREF: sub_14000B73C+77p
					; sub_14000B73C+B1p ...

var_30		= dword	ptr -30h
var_28		= qword	ptr -28h
var_20		= qword	ptr -20h
var_18		= qword	ptr -18h
var_10		= qword	ptr -10h
var_8		= qword	ptr -8
arg_10		= qword	ptr  40h

num_of_processors = edi
processor_idx =	ebx
		mov	[rsp-28h+arg_10], rbx
		push	rbp
		push	rsi
		push	rdi
		push	r14
		push	r15
		mov	rbp, rsp
		sub	rsp, 50h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rbp+var_8], rax
		mov	r14, rcx
		mov	r15, rdx
		mov	ecx, 0FFFFh
		call	cs:KeQueryActiveProcessorCountEx
		xor	processor_idx, processor_idx
		mov	num_of_processors, eax
		test	eax, eax
		jz	short loc_14000B6C3

loc_14000B65E:				; CODE XREF: execute_func_on_each_proc+9Dj
		xor	eax, eax
		lea	rdx, [rbp+var_30]
		mov	ecx, processor_idx
		mov	[rbp+var_30], eax
		call	KeGetProcessorNumberFromIndex
		test	eax, eax
		js	short loc_14000B6C5
		mov	cl, byte ptr [rbp+var_30+2]
		lea	rdx, [rbp+var_18]
		xor	eax, eax
		mov	[rbp+var_20], rax
		movzx	eax, word ptr [rbp+var_30]
		mov	word ptr [rbp+var_20], ax
		mov	eax, 1
		shl	rax, cl
		lea	rcx, [rbp+var_28]
		mov	[rbp+var_28], rax
		xor	eax, eax
		mov	[rbp+var_18], rax
		mov	[rbp+var_10], rax
		call	cs:KeSetSystemGroupAffinityThread
		mov	rcx, r15
		call	r14
		lea	rcx, [rbp+var_18]
		mov	esi, eax
		call	cs:KeRevertToUserGroupAffinityThread
		test	esi, esi
		js	short loc_14000B6E5
		inc	processor_idx
		cmp	processor_idx, num_of_processors
		jb	short loc_14000B65E

loc_14000B6C3:				; CODE XREF: execute_func_on_each_proc+38j
		xor	eax, eax

loc_14000B6C5:				; CODE XREF: execute_func_on_each_proc+4Cj
					; execute_func_on_each_proc+C3j
		mov	rcx, [rbp+var_8]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		mov	rbx, [rsp+50h+arg_10]
		add	rsp, 50h
		pop	r15
		pop	r14
		pop	rdi
		pop	rsi
		pop	rbp
		retn
; ---------------------------------------------------------------------------

loc_14000B6E5:				; CODE XREF: execute_func_on_each_proc+97j
		mov	eax, esi
		jmp	short loc_14000B6C5
execute_func_on_each_proc endp

; ---------------------------------------------------------------------------
algn_14000B6E9:				; DATA XREF: .pdata:000000014000A42Co
		align 4

; =============== S U B	R O U T	I N E =======================================


; __int64 __fastcall get_routine_address(PCWSTR	SourceString)
get_routine_address proc near		; CODE XREF: set_func_and_page_table_pointers+71p
					; set_func_and_page_table_pointers+1BCp
					; DATA XREF: ...

DestinationString= UNICODE_STRING ptr -18h

		sub	rsp, 38h
		xor	eax, eax
		mov	rdx, rcx	; SourceString
		lea	rcx, [rsp+38h+DestinationString] ; DestinationString
		mov	qword ptr [rsp+38h+DestinationString.Length], rax
		mov	[rsp+38h+DestinationString.Buffer], rax
		call	cs:RtlInitUnicodeString
		lea	rcx, [rsp+38h+DestinationString] ; SystemRoutineName
		call	cs:MmGetSystemRoutineAddress
		add	rsp, 38h
		retn
get_routine_address endp

; ---------------------------------------------------------------------------
algn_14000B71A:				; DATA XREF: .pdata:000000014000A438o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000B71C	proc near		; CODE XREF: new_unload_func+9p
					; main_run_stuff+A6p
					; DATA XREF: ...
		sub	rsp, 28h
		mov	rcx, cs:P	; P
		test	rcx, rcx
		jz	short loc_14000B737
		mov	edx, 56484C46h	; Tag
		call	cs:ExFreePoolWithTag

loc_14000B737:				; CODE XREF: sub_14000B71C+Ej
		add	rsp, 28h
		retn
sub_14000B71C	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

sub_14000B73C	proc near		; CODE XREF: main_run_stuff:loc_14000D09Bp
					; DATA XREF: .pdata:000000014000A444o ...

arg_0		= qword	ptr  10h

		mov	[rsp-8+arg_0], rbx
		push	rbp
		mov	rbp, rsp
		sub	rsp, 30h
		xor	ecx, ecx
		mov	eax, 1
		cpuid
		test	ecx, ecx
		jns	short loc_14000B770
		xor	ecx, ecx
		mov	eax, 40000001h
		cpuid
		cmp	eax, 56484C46h
		jnz	short loc_14000B770
		mov	eax, 0C0000120h
		jmp	loc_14000B80F
; ---------------------------------------------------------------------------

loc_14000B770:				; CODE XREF: sub_14000B73C+18j
					; sub_14000B73C+28j
		xor	ecx, ecx
		mov	eax, 1
		cpuid
		test	cl, 20h
		jz	loc_14000B80A
		mov	ecx, 480h
		call	read_some_msr
		shr	rax, 20h
		shr	eax, 12h
		and	al, 0Fh
		cmp	al, 6
		jnz	short loc_14000B80A
		mov	ecx, 3Ah
		call	read_some_msr
		mov	rbx, rax
		test	al, 1
		jnz	short loc_14000B7BC
		xor	edx, edx
		lea	rcx, wmsr_stuff
		call	execute_func_on_each_proc ; arg0 = init_s0_data()
		test	eax, eax
		js	short loc_14000B80A

loc_14000B7BC:				; CODE XREF: sub_14000B73C+6Cj
		test	bl, 4
		jz	short loc_14000B80A
		call	sub_14000B5A4
		test	al, al
		jz	short loc_14000B80A
		call	init_s0_data
		mov	rbx, rax
		test	rax, rax
		jnz	short loc_14000B7DE
		mov	eax, 0C00000A0h
		jmp	short loc_14000B80F
; ---------------------------------------------------------------------------

loc_14000B7DE:				; CODE XREF: sub_14000B73C+99j
		call	sub_14000B330
		mov	rdx, rbx
		lea	rcx, gogolaunch_wrap
		call	execute_func_on_each_proc ; arg0 = init_s0_data()
		mov	ebx, eax
		test	eax, eax
		jns	short loc_14000B80F
		xor	edx, edx
		lea	rcx, sub_14000C638
		call	execute_func_on_each_proc ; arg0 = init_s0_data()
		mov	eax, ebx
		jmp	short loc_14000B80F
; ---------------------------------------------------------------------------

loc_14000B80A:				; CODE XREF: sub_14000B73C+40j
					; sub_14000B73C+5Bj ...
		mov	eax, 0C035001Eh

loc_14000B80F:				; CODE XREF: sub_14000B73C+2Fj
					; sub_14000B73C+A0j ...
		mov	rbx, [rsp+30h+arg_0]
		add	rsp, 30h
		pop	rbp
		retn
sub_14000B73C	endp

; ---------------------------------------------------------------------------
algn_14000B81A:				; DATA XREF: .pdata:000000014000A450o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000B81C	proc near		; CODE XREF: new_unload_func+4p
		xor	edx, edx
		lea	rcx, sub_14000C638
		jmp	execute_func_on_each_proc ; arg0 = init_s0_data()
sub_14000B81C	endp

; ---------------------------------------------------------------------------
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000B82C	proc near		; CODE XREF: init_s0_data+3Fp
					; DATA XREF: .pdata:000000014000A45Co

BitMapHeader	= RTL_BITMAP ptr -38h
var_28		= RTL_BITMAP ptr -28h
StartingIndex	= dword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h

		push	rbx
		push	rsi
		push	rdi
		sub	rsp, 40h
		mov	edx, 1000h	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		mov	r8d, 56484C46h	; Tag
		call	cs:ExAllocatePoolWithTag
		mov	rdi, rax
		mov	[rsp+58h+arg_8], rax
		xor	ebx, ebx
		test	rax, rax
		jz	loc_14000B945
		xor	edx, edx
		mov	r8d, 1000h
		mov	rcx, rdi
		call	init_memory
		lea	rsi, [rdi+400h]
		mov	[rsp+58h+arg_10], rsi
		mov	edx, 0FFh
		mov	r8d, 400h
		mov	rcx, rdi
		call	init_memory
		mov	edx, 0FFh
		mov	r8d, 400h
		mov	rcx, rsi
		call	init_memory
		xor	eax, eax
		mov	qword ptr [rsp+58h+BitMapHeader.SizeOfBitMap], rax
		mov	[rsp+58h+BitMapHeader.Buffer], rax
		mov	r8d, 2000h	; SizeOfBitMap
		mov	rdx, rdi	; BitMapBuffer
		lea	rcx, [rsp+58h+BitMapHeader] ; BitMapHeader
		call	cs:RtlInitializeBitMap
		mov	edx, 0E7h	; StartingIndex
		mov	r8d, 2		; NumberToClear
		lea	rcx, [rsp+58h+BitMapHeader] ; BitMapHeader
		call	cs:RtlClearBits

loc_14000B8D2:				; CODE XREF: sub_14000B82C+DEj
		mov	[rsp+58h+StartingIndex], ebx
		cmp	ebx, 1000h
		jnb	short loc_14000B90C

loc_14000B8DE:				; DATA XREF: .rdata:0000000140006854o
		mov	ecx, ebx
		call	read_some_msr
		jmp	short loc_14000B908
; ---------------------------------------------------------------------------

loc_14000B8E7:				; DATA XREF: .rdata:0000000140006854o
		mov	r8d, 1		; NumberToClear
		mov	ebx, [rsp+58h+StartingIndex]
		mov	edx, ebx	; StartingIndex
		lea	rcx, [rsp+58h+BitMapHeader] ; BitMapHeader
		call	cs:RtlClearBits
		mov	rdi, [rsp+58h+arg_8]
		mov	rsi, [rsp+58h+arg_10]

loc_14000B908:				; CODE XREF: sub_14000B82C+B9j
		inc	ebx
		jmp	short loc_14000B8D2
; ---------------------------------------------------------------------------

loc_14000B90C:				; CODE XREF: sub_14000B82C+B0j
		xor	eax, eax
		mov	qword ptr [rsp+58h+var_28.SizeOfBitMap], rax
		mov	[rsp+58h+var_28.Buffer], rax
		mov	r8d, 2000h	; SizeOfBitMap
		mov	rdx, rsi	; BitMapBuffer
		lea	rcx, [rsp+58h+var_28] ;	BitMapHeader
		call	cs:RtlInitializeBitMap
		mov	edx, 101h	; StartingIndex
		mov	r8d, 2		; NumberToClear
		lea	rcx, [rsp+58h+var_28] ;	BitMapHeader
		call	cs:RtlClearBits
		mov	rax, rdi

loc_14000B945:				; CODE XREF: sub_14000B82C+28j
		add	rsp, 40h
		pop	rdi
		pop	rsi
		pop	rbx
		retn
sub_14000B82C	endp

; ---------------------------------------------------------------------------
algn_14000B94D:				; DATA XREF: .pdata:000000014000A45Co
		align 10h

; =============== S U B	R O U T	I N E =======================================


; __int64 __fastcall sub_14000B950(PVOID P)
sub_14000B950	proc near		; CODE XREF: gogolaunch+1FCp
					; sub_14000C638+38p
					; DATA XREF: ...

arg_0		= qword	ptr  8

		test	rcx, rcx
		jz	locret_14000BA05
		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		mov	rbx, rcx
		mov	rcx, [rcx+8]
		test	rcx, rcx
		jz	short loc_14000B974
		call	MmFreeContiguousMemory

loc_14000B974:				; CODE XREF: sub_14000B950+1Dj
		mov	rcx, [rbx+18h]	; P
		mov	edi, 56484C46h
		test	rcx, rcx
		jz	short loc_14000B98A
		mov	edx, edi	; Tag
		call	cs:ExFreePoolWithTag

loc_14000B98A:				; CODE XREF: sub_14000B950+30j
		mov	rcx, [rbx+10h]	; P
		test	rcx, rcx
		jz	short loc_14000B99B
		mov	edx, edi	; Tag
		call	cs:ExFreePoolWithTag

loc_14000B99B:				; CODE XREF: sub_14000B950+41j
		mov	rcx, [rbx+20h]
		test	rcx, rcx
		jz	short loc_14000B9A9
		call	sub_1400027C4

loc_14000B9A9:				; CODE XREF: sub_14000B950+52j
		mov	rcx, [rbx]
		test	rcx, rcx
		jz	short loc_14000B9F0
		or	eax, 0FFFFFFFFh
		lock xadd [rcx], eax
		cmp	eax, 1
		jnz	short loc_14000B9F0
		mov	rax, [rbx]
		mov	rcx, [rax+10h]	; P
		test	rcx, rcx
		jz	short loc_14000B9D1
		mov	edx, edi	; Tag
		call	cs:ExFreePoolWithTag

loc_14000B9D1:				; CODE XREF: sub_14000B950+77j
		mov	rax, [rbx]
		mov	rcx, [rax+8]	; P
		test	rcx, rcx
		jz	short loc_14000B9E5
		mov	edx, edi	; Tag
		call	cs:ExFreePoolWithTag

loc_14000B9E5:				; CODE XREF: sub_14000B950+8Bj
		mov	rcx, [rbx]	; P
		mov	edx, edi	; Tag
		call	cs:ExFreePoolWithTag

loc_14000B9F0:				; CODE XREF: sub_14000B950+5Fj
					; sub_14000B950+6Bj
		mov	edx, edi	; Tag
		mov	rcx, rbx	; P
		call	cs:ExFreePoolWithTag
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi

locret_14000BA05:			; CODE XREF: sub_14000B950+3j
		retn
sub_14000B950	endp

; ---------------------------------------------------------------------------
algn_14000BA06:				; DATA XREF: .pdata:000000014000A468o
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_14000BA08	proc near		; CODE XREF: sub_14000BE30+487p
					; sub_14000BE30+4A0p ...
		sub	rsp, 28h
		xor	eax, eax
		test	cx, cx
		jz	short loc_14000BA26
		movzx	ecx, cx
		call	near ptr word_14000152E
		shr	rax, 8
		and	eax, 0F0FFh
		jmp	short loc_14000BA2A
; ---------------------------------------------------------------------------

loc_14000BA26:				; CODE XREF: sub_14000BA08+9j
		bts	eax, 10h

loc_14000BA2A:				; CODE XREF: sub_14000BA08+1Cj
		add	rsp, 28h
		retn
sub_14000BA08	endp

; ---------------------------------------------------------------------------
algn_14000BA2F:				; DATA XREF: .pdata:000000014000A474o
		align 10h

; =============== S U B	R O U T	I N E =======================================


sub_14000BA30	proc near		; CODE XREF: sub_14000BE30+642p
					; sub_14000BE30+660p ...

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		movzx	ebx, dx
		mov	rdi, rcx
		test	dx, dx
		jnz	short loc_14000BA49
		xor	eax, eax
		jmp	short loc_14000BA80
; ---------------------------------------------------------------------------

loc_14000BA49:				; CODE XREF: sub_14000BA30+13j
		test	bl, 4
		jz	short loc_14000BA70
		call	sub_1400014F0
		movzx	ecx, ax
		shr	rcx, 3
		lea	rcx, [rdi+rcx*8]
		call	sub_14000BA8C
		movzx	ecx, bx
		shr	rcx, 3
		lea	rcx, [rax+rcx*8]
		jmp	short loc_14000BA7B
; ---------------------------------------------------------------------------

loc_14000BA70:				; CODE XREF: sub_14000BA30+1Cj
		movzx	eax, bx
		shr	rax, 3
		lea	rcx, [rcx+rax*8]

loc_14000BA7B:				; CODE XREF: sub_14000BA30+3Ej
		call	sub_14000BA8C

loc_14000BA80:				; CODE XREF: sub_14000BA30+17j
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
sub_14000BA30	endp

; ---------------------------------------------------------------------------
algn_14000BA8B:				; DATA XREF: .pdata:000000014000A480o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000BA8C	proc near		; CODE XREF: sub_14000BA30+2Ep
					; sub_14000BA30:loc_14000BA7Bp
		movzx	eax, byte ptr [rcx+4]
		movzx	r8d, byte ptr [rcx+7]
		movzx	edx, word ptr [rcx+2]
		shl	r8, 8
		or	r8, rax
		mov	rax, 100000000000h
		shl	r8, 10h
		or	r8, rdx
		test	[rcx], rax
		jnz	short loc_14000BAC0
		mov	ecx, [rcx+8]
		shl	rcx, 20h
		or	r8, rcx

loc_14000BAC0:				; CODE XREF: sub_14000BA8C+28j
		mov	rax, r8
		retn
sub_14000BA8C	endp


; =============== S U B	R O U T	I N E =======================================


init_s0_data	proc near		; CODE XREF: sub_14000B73C+8Ep
					; DATA XREF: .pdata:000000014000A48Co

BitMapHeader	= RTL_BITMAP ptr -28h
var_18		= RTL_BITMAP ptr -18h
arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h

		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rsi
		push	rdi
		sub	rsp, 40h
		mov	ebx, 56484C46h
		mov	esi, 20h
		mov	r8d, ebx	; Tag
		mov	edx, esi	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	rdi, rax
		test	rax, rax
		jz	loc_14000BBB8
		mov	r8d, esi
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		call	sub_14000B82C
		mov	[rdi+8], rax
		test	rax, rax
		jz	loc_14000BBAD
		mov	r8d, ebx	; Tag
		mov	edx, 2000h	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	rsi, rax
		test	rax, rax
		jz	short loc_14000BBA1
		xor	edx, edx
		lea	rbx, [rax+1000h]
		mov	r8d, 1000h
		mov	rcx, rax
		call	init_memory
		xor	edx, edx
		mov	r8d, 1000h
		mov	rcx, rbx
		call	init_memory
		xor	eax, eax
		lea	rcx, [rsp+48h+BitMapHeader] ; BitMapHeader
		mov	r8d, 8000h	; SizeOfBitMap
		mov	qword ptr [rsp+48h+BitMapHeader.SizeOfBitMap], rax
		mov	rdx, rsi	; BitMapBuffer
		mov	[rsp+48h+BitMapHeader.Buffer], rax
		call	cs:RtlInitializeBitMap
		xor	eax, eax
		lea	rcx, [rsp+48h+var_18] ;	BitMapHeader
		mov	r8d, 8000h	; SizeOfBitMap
		mov	qword ptr [rsp+48h+var_18.SizeOfBitMap], rax
		mov	rdx, rbx	; BitMapBuffer
		mov	[rsp+48h+var_18.Buffer], rax
		call	cs:RtlInitializeBitMap
		mov	rax, rdi
		mov	[rdi+10h], rsi
		mov	[rdi+18h], rbx
		jmp	short loc_14000BBBA
; ---------------------------------------------------------------------------

loc_14000BBA1:				; CODE XREF: init_s0_data+67j
		mov	rcx, [rdi+8]	; P
		mov	edx, ebx	; Tag
		call	cs:ExFreePoolWithTag

loc_14000BBAD:				; CODE XREF: init_s0_data+4Bj
		mov	edx, ebx	; Tag
		mov	rcx, rdi	; P
		call	cs:ExFreePoolWithTag

loc_14000BBB8:				; CODE XREF: init_s0_data+2Cj
		xor	eax, eax

loc_14000BBBA:				; CODE XREF: init_s0_data+DBj
		mov	rbx, [rsp+48h+arg_0]
		mov	rsi, [rsp+48h+arg_8]
		add	rsp, 40h
		pop	rdi
		retn
init_s0_data	endp

; ---------------------------------------------------------------------------
algn_14000BBCA:				; DATA XREF: .pdata:000000014000A48Co
		align 4

; =============== S U B	R O U T	I N E =======================================

; r8 = init_s0_data
; rdx =	some_args1

gogolaunch	proc near		; DATA XREF: .pdata:000000014000A498o
					; gogolaunch_wrap+7o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		test	r8, r8
		jz	locret_14000BDDF
		mov	[rsp+arg_0], rbx
		mov	[rsp+arg_8], rbp
		push	rsi
		push	rdi
		push	r14
		sub	rsp, 20h
		mov	rbx, r8
		mov	rsi, rdx
		mov	rbp, rcx
		mov	r14d, 56484C46h
		mov	r8d, r14d	; Tag
		mov	edx, 28h	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	rdi, rax
		test	rax, rax
		jz	loc_14000BDCD
		xor	edx, edx
		mov	rcx, rax
		lea	r8d, [rdx+28h]
		call	init_memory
		mov	[rdi], rbx
		lock inc dword ptr [rbx]
		call	init_CSTRUCT_0x20
		mov	[rdi+20h], rax
		test	rax, rax
		jz	loc_14000BDC5
		mov	ebx, 6000h
		mov	ecx, ebx
		call	INIT_HOST_RSP
		mov	[rdi+8], rax	; HOST_RSP
		test	rax, rax
		jz	loc_14000BDC5
		mov	r8d, ebx
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		mov	ebx, 1000h
		mov	r8d, r14d	; Tag
		mov	edx, ebx	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	[rdi+18h], rax
		test	rax, rax
		jz	loc_14000BDC5
		mov	r8d, ebx
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		mov	r8d, r14d	; Tag
		mov	edx, ebx	; NumberOfBytes
		xor	ecx, ecx	; PoolType
		call	cs:ExAllocatePoolWithTag
		mov	[rdi+10h], rax
		test	rax, rax
		jz	loc_14000BDC5
		mov	r8d, ebx
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		mov	rax, [rdi+8]
		mov	ecx, 486h
		lea	r14, [rax+5FF0h] ; HOST_RSP
		or	qword ptr [r14], 0FFFFFFFFFFFFFFFFh
		mov	[rax+5FF8h], rdi
		call	read_some_msr
		mov	ecx, 487h
		mov	rbx, rax
		call	read_some_msr
		mov	rcx, cr0
		and	rcx, rax
		or	rcx, rbx
		mov	cr0, rcx
		mov	ecx, 488h
		call	read_some_msr
		mov	ecx, 489h
		mov	rbx, rax
		call	read_some_msr
		mov	rcx, cr4
		and	rcx, rax
		or	rcx, rbx
		mov	cr4, rcx
		mov	ebx, 480h
		mov	ecx, ebx
		call	read_some_msr
		mov	rdx, [rdi+10h]
		btr	eax, 1Fh
		mov	[rdx], eax
		mov	rcx, [rdi+10h]
		call	MmGetPhysicalAddress
		mov	[rsp+38h+arg_18], rax
		vmxon	[rsp+38h+arg_18]
		jbe	loc_14000BDC5
		call	sub_140002D30
		call	sub_140002D70
		mov	ecx, ebx
		call	read_some_msr
		mov	rcx, [rdi+18h]
		btr	eax, 1Fh
		mov	[rcx], eax
		mov	rcx, [rdi+18h]
		call	MmGetPhysicalAddress
		mov	[rsp+38h+arg_10], rax
		vmclear	[rsp+38h+arg_10]
		jbe	short loc_14000BDC2
		vmptrld	[rsp+38h+arg_10]
		setz	cl
		setb	al
		adc	cl, al
		jnz	short loc_14000BDC2
		mov	r9, r14		; HOST_RSP
		mov	r8, rsi
		mov	rdx, rbp
		mov	rcx, rdi
		call	sub_14000BE30	; r8=some_args1
		test	al, al
		jz	short loc_14000BDC2
		mov	ebx, 4400h
		mov	ecx, ebx
		call	do_vm_read
		vmlaunch
		setz	dl
		setb	al
		adc	dl, al
		cmp	dl, 1
		jnz	short loc_14000BDB5
		mov	ecx, ebx
		call	do_vm_read

loc_14000BDB5:				; CODE XREF: gogolaunch+1E0j
		mov	rax, cs:KdDebuggerNotPresent
		cmp	byte ptr [rax],	0
		jnz	short loc_14000BDC2
		int	3		; Trap to Debugger

loc_14000BDC2:				; CODE XREF: gogolaunch+1A0j
					; gogolaunch+1AFj ...
		vmxoff

loc_14000BDC5:				; CODE XREF: gogolaunch+66j
					; gogolaunch+7Fj ...
		mov	rcx, rdi	; P
		call	sub_14000B950

loc_14000BDCD:				; CODE XREF: gogolaunch+40j
		mov	rbx, [rsp+38h+arg_0]
		mov	rbp, [rsp+38h+arg_8]
		add	rsp, 20h
		pop	r14
		pop	rdi
		pop	rsi

locret_14000BDDF:			; CODE XREF: gogolaunch+3j
		retn
gogolaunch	endp


; =============== S U B	R O U T	I N E =======================================


wmsr_stuff	proc near		; DATA XREF: .pdata:000000014000A498o
					; .pdata:000000014000A4A4o ...

arg_8		= qword	ptr  10h

		sub	rsp, 28h
		mov	ecx, 3Ah
		call	read_some_msr
		mov	[rsp+28h+arg_8], rax
		test	al, 1
		jz	short loc_14000BDFB
		xor	eax, eax
		jmp	short loc_14000BE28
; ---------------------------------------------------------------------------

loc_14000BDFB:				; CODE XREF: wmsr_stuff+15j
		or	eax, 1
		mov	ecx, 3Ah
		mov	dword ptr [rsp+28h+arg_8], eax
		mov	rdx, [rsp+28h+arg_8]
		call	sub_140002FD8
		mov	ecx, 3Ah
		call	read_some_msr
		and	al, 1
		neg	al
		sbb	eax, eax
		not	eax
		and	eax, 0C0000182h

loc_14000BE28:				; CODE XREF: wmsr_stuff+19j
		add	rsp, 28h
		retn
wmsr_stuff	endp

; ---------------------------------------------------------------------------
algn_14000BE2D:				; DATA XREF: .pdata:000000014000A4A4o
		align 10h

; =============== S U B	R O U T	I N E =======================================

; r8=some_args1
; Attributes: bp-based frame fpd=0B0h

sub_14000BE30	proc near		; CODE XREF: gogolaunch+1BDp
					; DATA XREF: .pdata:000000014000A4B0o

var_B0		= qword	ptr -0B0h
var_A8		= qword	ptr -0A8h
var_A0		= qword	ptr -0A0h
var_98		= qword	ptr -98h
var_90		= qword	ptr -90h
var_88		= qword	ptr -88h
var_80		= qword	ptr -80h
host_rsp	= qword	ptr -78h
var_70		= qword	ptr -70h
var_68		= word ptr -68h
var_60		= qword	ptr -60h
var_58		= word ptr -58h
var_50		= qword	ptr -50h

		push	rbp
		push	rbx
		push	rsi
		push	rdi
		push	r12
		push	r13
		push	r14
		push	r15
		sub	rsp, 98h
		lea	rbp, [rsp+20h]
		mov	rax, cs:__security_cookie
		xor	rax, rbp
		mov	[rbp+0B0h+var_50], rax
		xor	eax, eax
		mov	[rbp+0B0h+var_B0], rcx
		lea	rcx, [rbp+0B0h+var_70]
		mov	[rbp+0B0h+var_70], rax
		mov	[rbp+0B0h+var_68], ax
		mov	[rbp+0B0h+host_rsp], r9
		mov	[rbp+0B0h+var_80], r8
		mov	[rbp+0B0h+var_88], rdx
		call	sub_1400014E8
		xor	eax, eax
		mov	[rbp+0B0h+var_60], rax
		mov	[rbp+0B0h+var_58], ax
		sidt	fword ptr [rbp+0B0h+var_60]
		mov	ecx, 480h
		call	read_some_msr
		mov	rdi, rax
		xor	ebx, ebx
		shr	rdi, 20h
		or	ebx, 4
		shr	edi, 17h
		and	edi, 1
		mov	ecx, edi
		neg	ecx
		sbb	ecx, ecx
		and	ecx, 0Ch
		add	ecx, 484h
		call	read_some_msr
		mov	r15, rax
		mov	ecx, 200h
		or	ebx, ecx
		shr	r15, 20h
		and	r15d, ebx
		xor	ebx, ebx
		or	ebx, ecx
		or	r15d, eax
		mov	eax, edi
		neg	eax
		sbb	ecx, ecx
		and	ecx, 0Ch
		add	ecx, 483h
		call	read_some_msr
		mov	r12, rax
		bts	ebx, 0Fh
		shr	r12, 20h
		and	r12d, ebx
		xor	ebx, ebx
		or	r12d, eax
		mov	eax, edi
		neg	eax
		sbb	ecx, ecx
		and	ecx, 0Ch
		add	ecx, 481h
		call	read_some_msr
		mov	r13, rax
		shr	r13, 20h
		and	r13d, ebx
		or	ebx, 12808000h
		or	r13d, eax
		neg	edi
		sbb	ecx, ecx
		and	ecx, 0Ch
		add	ecx, 482h
		call	read_some_msr
		bts	ebx, 1Fh
		mov	rcx, rax
		shr	rcx, 20h
		and	ecx, ebx
		xor	ebx, ebx
		or	ecx, eax
		or	ebx, 102Eh
		mov	[rbp+0B0h+var_98], rcx
		mov	ecx, 48Bh
		call	read_some_msr
		bts	ebx, 14h
		mov	rcx, rax
		shr	rcx, 20h
		and	ecx, ebx
		or	ecx, eax
		xor	ebx, ebx
		mov	[rbp+0B0h+var_90], rcx
		mov	[rbp+0B0h+var_A8], rbx
		mov	rsi, cr0
		xor	edi, edi
		mov	[rbp+0B0h+var_A0], rdi
		mov	r14, cr4
		call	sub_140002E38
		test	al, al
		jz	short loc_14000BF9A
		or	dword ptr [rbp+0B0h+var_A8], 0E0000000h
		or	dword ptr [rbp+0B0h+var_A0], 1000B0h
		mov	rdi, [rbp+0B0h+var_A0]
		mov	rbx, [rbp+0B0h+var_A8]

loc_14000BF9A:				; CODE XREF: sub_14000BE30+152j
		xor	ecx, ecx
		call	cs:KeGetCurrentProcessorNumberEx
		xor	ecx, ecx
		lea	edx, [rax+1]
		call	do_vm_write
		call	near ptr loc_140001500+2
		movzx	edx, ax
		mov	ecx, 800h
		call	do_vm_write
		call	sub_14000150A
		movzx	edx, ax
		mov	ecx, 802h
		call	do_vm_write
		call	sub_140001512
		movzx	edx, ax
		mov	ecx, 804h
		call	do_vm_write
		call	sub_14000151A
		movzx	edx, ax
		mov	ecx, 806h
		call	do_vm_write
		call	sub_140001522
		movzx	edx, ax
		mov	ecx, 808h
		call	do_vm_write
		call	near ptr byte_140001528+2
		movzx	edx, ax
		mov	ecx, 80Ah
		call	do_vm_write
		call	sub_1400014F0
		movzx	edx, ax
		mov	ecx, 80Ch
		call	do_vm_write
		call	sub_1400014F9
		movzx	edx, ax
		mov	ecx, 80Eh
		call	do_vm_write
		call	near ptr loc_140001500+2
		movzx	edx, ax
		mov	ecx, 0C00h
		and	edx, 0F8h
		call	do_vm_write
		call	sub_14000150A
		movzx	edx, ax
		mov	ecx, 0C02h
		and	edx, 0F8h
		call	do_vm_write
		call	sub_140001512
		movzx	edx, ax
		mov	ecx, 0C04h
		and	edx, 0F8h
		call	do_vm_write
		call	sub_14000151A
		movzx	edx, ax
		mov	ecx, 0C06h
		and	edx, 0F8h
		call	do_vm_write
		call	sub_140001522
		movzx	edx, ax
		mov	ecx, 0C08h
		and	edx, 0F8h
		call	do_vm_write
		call	near ptr byte_140001528+2
		movzx	edx, ax
		mov	ecx, 0C0Ah
		and	edx, 0F8h
		call	do_vm_write
		call	sub_1400014F9
		movzx	edx, ax
		mov	ecx, 0C0Ch
		and	edx, 0F8h
		call	do_vm_write
		mov	rax, [rbp+0B0h+var_B0]
		mov	rcx, [rax]
		mov	rcx, [rcx+10h]
		call	MmGetPhysicalAddress
		mov	rdx, rax
		mov	ecx, 2000h
		call	do_vm_write
		mov	rax, [rbp+0B0h+var_B0]
		mov	rcx, [rax]
		mov	rcx, [rcx+18h]
		call	MmGetPhysicalAddress
		mov	rdx, rax
		mov	ecx, 2002h
		call	do_vm_write
		mov	rax, [rbp+0B0h+var_B0]
		mov	rcx, [rax]
		mov	rcx, [rcx+8]
		call	MmGetPhysicalAddress
		mov	rdx, rax
		mov	ecx, 2004h
		call	do_vm_write
		mov	rax, [rbp+0B0h+var_B0]
		mov	rcx, [rax+20h]
		call	sub_1400026A8
		mov	rdx, rax
		mov	ecx, 201Ah
		call	do_vm_write
		or	rdx, 0FFFFFFFFFFFFFFFFh
		mov	ecx, 2800h
		call	do_vm_write
		mov	ecx, 1D9h
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 2802h
		call	do_vm_write
		call	sub_140002E38
		test	al, al
		jz	short loc_14000C18B
		mov	rcx, cr3
		call	sub_140002E3C

loc_14000C18B:				; CODE XREF: sub_14000BE30+351j
		mov	edx, r13d
		mov	ecx, 4000h
		call	do_vm_write
		mov	edx, dword ptr [rbp+0B0h+var_98]
		mov	ecx, 4002h
		call	do_vm_write
		mov	edx, 2
		mov	ecx, 4004h
		call	do_vm_write
		mov	edx, r12d
		mov	ecx, 400Ch
		call	do_vm_write
		mov	edx, r15d
		mov	ecx, 4012h
		call	do_vm_write
		mov	edx, dword ptr [rbp+0B0h+var_90]
		mov	ecx, 401Eh
		call	do_vm_write
		call	near ptr loc_140001500+2
		movzx	eax, ax
		mov	ecx, 4800h
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		call	sub_14000150A
		movzx	eax, ax
		mov	ecx, 4802h
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		call	sub_140001512
		movzx	eax, ax
		mov	ecx, 4804h
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		call	sub_14000151A
		movzx	eax, ax
		mov	ecx, 4806h
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		call	sub_140001522
		movzx	eax, ax
		mov	ecx, 4808h
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		call	near ptr byte_140001528+2
		movzx	eax, ax
		mov	ecx, 480Ah
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		call	sub_1400014F0
		movzx	eax, ax
		mov	ecx, 480Ch
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		call	sub_1400014F9
		movzx	eax, ax
		mov	ecx, 480Eh
		lsl	edx, eax
		mov	edx, edx
		call	do_vm_write
		movzx	edx, word ptr [rbp+0B0h+var_70]
		mov	ecx, 4810h
		call	do_vm_write
		movzx	edx, word ptr [rbp+0B0h+var_60]
		mov	ecx, 4812h
		call	do_vm_write
		call	near ptr loc_140001500+2
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 4814h
		call	do_vm_write
		call	sub_14000150A
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 4816h
		call	do_vm_write
		call	sub_140001512
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 4818h
		call	do_vm_write
		call	sub_14000151A
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 481Ah
		call	do_vm_write
		call	sub_140001522
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 481Ch
		call	do_vm_write
		call	near ptr byte_140001528+2
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 481Eh
		call	do_vm_write
		call	sub_1400014F0
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 4820h
		call	do_vm_write
		call	sub_1400014F9
		movzx	ecx, ax
		call	sub_14000BA08
		mov	edx, eax
		mov	ecx, 4822h
		call	do_vm_write
		mov	r15d, 174h
		mov	ecx, r15d
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 482Ah
		call	do_vm_write
		mov	ecx, r15d
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 4C00h
		call	do_vm_write
		mov	rdx, rbx
		mov	ecx, 6000h
		call	do_vm_write
		mov	rdx, rdi
		mov	ecx, 6002h
		call	do_vm_write
		mov	rdx, rsi
		mov	ecx, 6004h
		call	do_vm_write
		mov	rdx, r14
		mov	ecx, 6006h
		call	do_vm_write
		mov	rdx, cr0
		mov	ecx, 6800h
		call	do_vm_write
		mov	rdx, cr3
		mov	ecx, 6802h
		call	do_vm_write
		mov	rdx, cr4
		mov	ecx, 6804h
		call	do_vm_write
		xor	edx, edx
		mov	ecx, 6806h
		call	do_vm_write
		xor	edx, edx
		mov	ecx, 6808h
		call	do_vm_write
		xor	edx, edx
		mov	ecx, 680Ah
		call	do_vm_write
		xor	edx, edx
		mov	ecx, 680Ch
		call	do_vm_write
		mov	r14d, 0C0000100h
		mov	ecx, r14d
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 680Eh
		call	do_vm_write
		mov	esi, 0C0000101h
		mov	ecx, esi
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 6810h
		call	do_vm_write
		call	sub_1400014F0
		mov	rcx, [rbp+0B0h+var_70+2]
		movzx	edx, ax
		call	sub_14000BA30
		mov	rdx, rax
		mov	ecx, 6812h
		call	do_vm_write
		call	sub_1400014F9
		mov	rcx, [rbp+0B0h+var_70+2]
		movzx	edx, ax
		call	sub_14000BA30
		mov	rdx, rax
		mov	ecx, 6814h
		call	do_vm_write
		mov	rdx, [rbp+0B0h+var_70+2]
		mov	ecx, 6816h
		call	do_vm_write
		mov	rdx, [rbp+0B0h+var_60+2]
		mov	ecx, 6818h
		call	do_vm_write
		mov	rdx, dr7
		mov	ecx, 681Ah
		call	do_vm_write
		mov	rdx, [rbp+0B0h+var_88]
		mov	ecx, 681Ch // GUEST_RSP
		call	do_vm_write
		mov	rdx, [rbp+0B0h+var_80]
		mov	ecx, 681Eh
		call	do_vm_write
		mov	ecx, 6820h
		pushfq
		pop	rdx
		call	do_vm_write
		lea	edi, [r15+1]
		mov	ecx, edi
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 6824h
		call	do_vm_write
		lea	ebx, [rdi+1]
		mov	ecx, ebx
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 6826h
		call	do_vm_write
		mov	rdx, cr0
		mov	ecx, 6C00h
		call	do_vm_write
		mov	rdx, cr3
		mov	ecx, 6C02h
		call	do_vm_write
		mov	rdx, cr4
		mov	ecx, 6C04h
		call	do_vm_write
		mov	ecx, r14d
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 6C06h
		call	do_vm_write
		mov	ecx, esi
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 6C08h
		call	do_vm_write
		call	sub_1400014F9
		mov	rcx, [rbp+0B0h+var_70+2]
		movzx	edx, ax
		call	sub_14000BA30
		mov	rdx, rax
		mov	ecx, 6C0Ah
		call	do_vm_write
		mov	rdx, [rbp+0B0h+var_70+2]
		mov	ecx, 6C0Ch
		call	do_vm_write
		mov	rdx, [rbp+0B0h+var_60+2]
		mov	ecx, 6C0Eh
		call	do_vm_write
		mov	ecx, edi
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 6C10h
		call	do_vm_write
		mov	ecx, ebx
		call	read_some_msr
		mov	rdx, rax
		mov	ecx, 6C12h
		call	do_vm_write
		mov	rdx, [rbp+0B0h+host_rsp] ; SET_HOST_RSP
		mov	ecx, 6C14h
		call	do_vm_write
		lea	rdx, ENTRY_FUNC
		mov	ecx, 6C16h
		call	do_vm_write
		mov	al, 1
		mov	rcx, [rbp+0B0h+var_50]
		xor	rcx, rbp	; BugCheckParameter1
		call	sub_140004B50
		lea	rsp, [rbp+78h]
		pop	r15
		pop	r14
		pop	r13
		pop	r12
		pop	rdi
		pop	rsi
		pop	rbx
		pop	rbp
		retn
sub_14000BE30	endp

; ---------------------------------------------------------------------------
algn_14000C613:				; DATA XREF: .pdata:000000014000A4B0o
		align 4

; =============== S U B	R O U T	I N E =======================================


gogolaunch_wrap	proc near		; DATA XREF: .pdata:000000014000A4BCo
					; sub_14000B73C+AAo
		sub	rsp, 28h
		mov	rdx, rcx
		lea	rcx, gogolaunch	; r8 = init_s0_data
					; rdx =	some_args1
		call	run_cb1
		neg	al
		sbb	eax, eax
		not	eax
		and	eax, 0C0000001h
		add	rsp, 28h
		retn
gogolaunch_wrap	endp

; ---------------------------------------------------------------------------
algn_14000C637:				; DATA XREF: .pdata:000000014000A4BCo
		align 8

; =============== S U B	R O U T	I N E =======================================


sub_14000C638	proc near		; DATA XREF: .pdata:000000014000A4C8o
					; sub_14000B73C+BEo ...

arg_8		= qword	ptr  10h
P		= qword	ptr  18h

		sub	rsp, 28h
		and	[rsp+28h+P], 0
		lea	rdx, [rsp+28h+P]
		mov	ecx, 13687455h
		call	vm_call_wrapper
		test	eax, eax
		js	short loc_14000C677
		mov	rax, cr4
		mov	[rsp+28h+arg_8], rax
		btr	dword ptr [rsp+28h+arg_8], 0Dh
		mov	rax, [rsp+28h+arg_8]
		mov	cr4, rax
		mov	rcx, [rsp+28h+P] ; P
		call	sub_14000B950
		xor	eax, eax

loc_14000C677:				; CODE XREF: sub_14000C638+1Bj
		add	rsp, 28h
		retn
sub_14000C638	endp

; ---------------------------------------------------------------------------
algn_14000C67C:				; DATA XREF: .pdata:000000014000A4C8o
		align 200h
		dq 100h	dup(?)
PAGE		ends

; Section 6. (virtual address 0000D000)
; Virtual size			: 00000A38 (   2616.)
; Section size in file		: 00000C00 (   3072.)
; Offset to raw	data for section: 00007200
; Flags	62000020: Text Discardable Executable Readable
; Alignment	: default
; ===========================================================================

; Segment type:	Pure code
; Segment permissions: Read/Execute
INIT		segment	para public 'CODE' use64
		assume cs:INIT
		;org 14000D000h
		assume es:nothing, ss:nothing, ds:_data, fs:nothing, gs:nothing

; =============== S U B	R O U T	I N E =======================================


main_run_stuff	proc near		; CODE XREF: drivermain+23p
					; drivermain+A4p
					; DATA XREF: ...

var_138		= dword	ptr -138h
var_134		= dword	ptr -134h
var_130		= dword	ptr -130h
var_18		= qword	ptr -18h
arg_8		= qword	ptr  10h

		mov	[rsp+arg_8], rbx
		push	rdi
		sub	rsp, 150h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+158h+var_18], rax
		lea	rax, new_unload_func
		mov	[rsp+158h+var_138], 114h
		mov	[rcx+68h], rax
		mov	rdi, rcx
		lea	rcx, [rsp+158h+var_138]
		call	cs:RtlGetVersion
		test	eax, eax
		js	short loc_14000D068
		cmp	[rsp+158h+var_134], 6
		ja	short loc_14000D054
		jnz	short loc_14000D068
		cmp	[rsp+158h+var_130], 2
		jb	short loc_14000D068

loc_14000D054:				; CODE XREF: main_run_stuff+49j
		mov	cs:dword_140007308, 200h
		mov	cs:dword_14000730C, 40000000h

loc_14000D068:				; CODE XREF: main_run_stuff+42j
					; main_run_stuff+4Bj ...
		call	more_version_check
		test	al, al
		jnz	short loc_14000D078
		mov	eax, 0C0000120h
		jmp	short loc_14000D0C1
; ---------------------------------------------------------------------------

loc_14000D078:				; CODE XREF: main_run_stuff+6Fj
		call	no_cb_called
		test	eax, eax
		js	short loc_14000D0C1
		mov	rcx, rdi
		call	set_func_and_page_table_pointers
		mov	ebx, eax
		test	eax, eax
		jns	short loc_14000D09B
		call	empty_linked_list_and_call_cb
		call	sub_14000B000
		jmp	short loc_14000D0BF
; ---------------------------------------------------------------------------

loc_14000D09B:				; CODE XREF: main_run_stuff+8Dj
		call	sub_14000B73C
		mov	ebx, eax
		test	eax, eax
		jns	short loc_14000D0B2
		call	sub_14000B71C
		call	empty_linked_list_and_call_cb
		jmp	short loc_14000D0BF
; ---------------------------------------------------------------------------

loc_14000D0B2:				; CODE XREF: main_run_stuff+A4j
		mov	rdx, rdi
		mov	ecx, 13687456h
		call	vm_call_wrapper

loc_14000D0BF:				; CODE XREF: main_run_stuff+99j
					; main_run_stuff+B0j
		mov	eax, ebx

loc_14000D0C1:				; CODE XREF: main_run_stuff+76j
					; main_run_stuff+7Fj
		mov	rcx, [rsp+158h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		mov	rbx, [rsp+158h+arg_8]
		add	rsp, 150h
		pop	rdi
		retn
main_run_stuff	endp

; ---------------------------------------------------------------------------
algn_14000D0E2:				; DATA XREF: .pdata:000000014000A4D4o
		align 4

; =============== S U B	R O U T	I N E =======================================


more_version_check proc	near		; CODE XREF: main_run_stuff:loc_14000D068p
					; DATA XREF: .pdata:000000014000A4E0o

var_138		= byte ptr -138h
var_134		= dword	ptr -134h
var_18		= qword	ptr -18h

		sub	rsp, 158h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+158h+var_18], rax
		xor	edx, edx
		lea	rcx, [rsp+158h+var_138]
		mov	r8d, 114h
		call	init_memory
		lea	rcx, [rsp+158h+var_138]
		call	cs:RtlGetVersion
		test	eax, eax
		jns	short loc_14000D122
		xor	al, al
		jmp	short loc_14000D131
; ---------------------------------------------------------------------------

loc_14000D122:				; CODE XREF: more_version_check+38j
		mov	eax, [rsp+158h+var_134]
		add	eax, 0FFFFFFFAh
		test	eax, 0FFFFFFFBh
		setz	al

loc_14000D131:				; CODE XREF: more_version_check+3Cj
		mov	rcx, [rsp+158h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		add	rsp, 158h
		retn
more_version_check endp

; ---------------------------------------------------------------------------
algn_14000D149:				; DATA XREF: .pdata:000000014000A4E0o
		align 4

; =============== S U B	R O U T	I N E =======================================


no_cb_called	proc near		; CODE XREF: main_run_stuff:loc_14000D078p
					; DATA XREF: .pdata:000000014000A4ECo

arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 20h
		lea	rbx, unk_140006148
		lea	rdi, unk_140006148
		jmp	short loc_14000D16C
; ---------------------------------------------------------------------------

loc_14000D166:				; CODE XREF: no_cb_called+23j
		call	qword ptr [rbx]
		add	rbx, 8

loc_14000D16C:				; CODE XREF: no_cb_called+18j
		cmp	rbx, rdi
		jb	short loc_14000D166
		xor	eax, eax
		mov	rbx, [rsp+28h+arg_0]
		add	rsp, 20h
		pop	rdi
		retn
no_cb_called	endp

; ---------------------------------------------------------------------------
algn_14000D17E:				; DATA XREF: .pdata:000000014000A4ECo
		align 20h

; =============== S U B	R O U T	I N E =======================================


set_func_and_page_table_pointers proc near ; CODE XREF:	main_run_stuff+84p
					; DATA XREF: .pdata:000000014000A4F8o

var_138		= dword	ptr -138h
var_134		= qword	ptr -134h
var_12C		= dword	ptr -12Ch
var_18		= qword	ptr -18h
arg_0		= qword	ptr  8

		mov	[rsp+arg_0], rbx
		push	rdi
		sub	rsp, 150h
		mov	rax, cs:__security_cookie
		xor	rax, rsp
		mov	[rsp+158h+var_18], rax
		mov	rdi, rcx
		mov	[rsp+158h+var_138], 114h
		lea	rcx, [rsp+158h+var_134]
		xor	edx, edx
		mov	r8d, 110h
		call	init_memory
		lea	rcx, [rsp+158h+var_138]
		call	cs:RtlGetVersion
		mov	ebx, eax
		test	eax, eax
		js	loc_14000D30A
		cmp	dword ptr [rsp+158h+var_134], 0Ah ; win10
		jb	loc_14000D270	; win10	or build < 14316
		cmp	[rsp+158h+var_12C], 37ECh
		jb	loc_14000D270	; win10	or build < 14316
		lea	rcx, SourceString ; "MmGetVirtualForPhysical"
		call	get_routine_address
		test	rax, rax
		jnz	short loc_14000D205

loc_14000D1FB:				; CODE XREF: set_func_and_page_table_pointers+A1j
		mov	eax, 0C000007Ah
		jmp	loc_14000D34A
; ---------------------------------------------------------------------------

loc_14000D205:				; CODE XREF: set_func_and_page_table_pointers+79j
		mov	r9d, 0Ah
		lea	r8, some_func_preambule
		mov	rcx, rax	; Source2
		lea	edx, [r9+26h]
		call	find_substring_pos ; (target_area, target_len, pattern,	pattern_len
		test	rax, rax
		jz	short loc_14000D1FB
		mov	r8, [rax+0Ah]
		mov	r9d, 1FFh
		mov	rdx, r8
		mov	cs:page_table_ptr4, r8
		shr	rdx, 27h
		and	rdx, r9
		mov	rcx, rdx
		mov	rax, rdx
		shl	rcx, 1Eh
		or	rcx, r8
		shl	rax, 15h
		or	rax, rcx
		shl	rdx, 0Ch
		or	rdx, rax
		mov	cs:page_table_ptr2, rax
		mov	cs:page_table_ptr1, rdx
		mov	cs:page_table_ptr3, rcx
		jmp	short loc_14000D2AE
; ---------------------------------------------------------------------------

loc_14000D270:				; CODE XREF: set_func_and_page_table_pointers+56j
					; set_func_and_page_table_pointers+64j
		mov	rax, cs:qword_140007000	; win10	or build < 14316
		mov	r9d, 1FFh
		mov	cs:page_table_ptr1, rax
		mov	rax, cs:qword_140007008
		mov	cs:page_table_ptr2, rax
		mov	rax, cs:qword_140007010
		mov	cs:page_table_ptr3, rax
		mov	rax, cs:qword_140007018
		mov	cs:page_table_ptr4, rax

loc_14000D2AE:				; CODE XREF: set_func_and_page_table_pointers+EEj
		mov	rax, 0FFFFFFFFFh
		mov	cs:qword_140008CA0, 7FFFFFFh
		mov	cs:main_page_table, rax
		mov	eax, ebx
		mov	cs:qword_140008C88, 0Ch
		mov	cs:qword_140008C80, 15h
		mov	cs:qword_140008C98, 3FFFFh
		mov	cs:qword_140008C90, r9
		mov	cs:qword_140008C78, 1Eh
		mov	cs:qword_140008C70, 27h

loc_14000D30A:				; CODE XREF: set_func_and_page_table_pointers+4Bj
		test	ebx, ebx
		js	short loc_14000D34A
		mov	rax, [rdi+28h]
		mov	rcx, [rax]
		lea	rax, sub_140002FE4
		mov	cs:qword_140008C30, rax
		mov	cs:qword_140008C38, rcx
		call	sub_14000D36C
		mov	ebx, eax
		test	eax, eax
		js	short loc_14000D34A
		lea	rcx, aMmallocatecont ; "MmAllocateContiguousNodeMemory"
		call	get_routine_address
		mov	cs:nm_allocate_contiguous_node_mem, rax
		mov	eax, ebx

loc_14000D34A:				; CODE XREF: set_func_and_page_table_pointers+80j
					; set_func_and_page_table_pointers+18Cj ...
		mov	rcx, [rsp+158h+var_18]
		xor	rcx, rsp	; BugCheckParameter1
		call	sub_140004B50
		mov	rbx, [rsp+158h+arg_0]
		add	rsp, 150h
		pop	rdi
		retn
set_func_and_page_table_pointers endp

; ---------------------------------------------------------------------------
algn_14000D36B:				; DATA XREF: .pdata:000000014000A4F8o
		align 4

; =============== S U B	R O U T	I N E =======================================


sub_14000D36C	proc near		; CODE XREF: set_func_and_page_table_pointers+1AAp
					; DATA XREF: .pdata:000000014000A504o

arg_0		= qword	ptr  8
arg_8		= qword	ptr  10h
arg_10		= qword	ptr  18h
arg_18		= qword	ptr  20h

		mov	rax, rsp
		mov	[rax+8], rbx
		mov	[rax+10h], rbp
		mov	[rax+18h], rsi
		mov	[rax+20h], rdi
		push	r14
		sub	rsp, 20h
		call	cs:MmGetPhysicalMemoryRanges
		mov	rbx, rax
		test	rax, rax
		jz	short loc_14000D3E0
		xor	edi, edi
		xor	r14d, r14d

loc_14000D398:				; CODE XREF: sub_14000D36C+60j
		mov	ecx, edi
		add	rcx, rcx
		cmp	qword ptr [rbx+rcx*8], 0
		jnz	short loc_14000D3AC
		cmp	qword ptr [rbx+rcx*8+8], 0
		jz	short loc_14000D3CE

loc_14000D3AC:				; CODE XREF: sub_14000D36C+36j
		mov	rcx, [rbx+rcx*8+8]
		mov	eax, 0
		test	rcx, 0FFFh
		setnz	al
		sar	rcx, 0Ch
		add	r14, rcx
		add	r14, rax
		inc	edi
		jmp	short loc_14000D398
; ---------------------------------------------------------------------------

loc_14000D3CE:				; CODE XREF: sub_14000D36C+3Ej
		test	edi, edi
		jnz	short loc_14000D400

loc_14000D3D2:				; CODE XREF: sub_14000D36C+B6j
		mov	edx, 68506D4Dh	; Tag
		mov	rcx, rbx	; P
		call	cs:ExFreePoolWithTag

loc_14000D3E0:				; CODE XREF: sub_14000D36C+25j
		mov	eax, 0C0000001h

loc_14000D3E5:				; CODE XREF: sub_14000D36C+128j
		mov	rbx, [rsp+28h+arg_0]
		mov	rbp, [rsp+28h+arg_8]
		mov	rsi, [rsp+28h+arg_10]
		mov	rdi, [rsp+28h+arg_18]
		add	rsp, 20h
		pop	r14
		retn
; ---------------------------------------------------------------------------

loc_14000D400:				; CODE XREF: sub_14000D36C+64j
		lea	ebp, [rdi-1]
		mov	r8d, 56484C46h	; Tag
		add	rbp, 2
		xor	ecx, ecx	; PoolType
		shl	rbp, 4
		mov	rdx, rbp	; NumberOfBytes
		call	cs:ExAllocatePoolWithTag
		mov	rsi, rax
		test	rax, rax
		jz	short loc_14000D3D2
		mov	r8, rbp
		xor	edx, edx
		mov	rcx, rax
		call	init_memory
		mov	[rsi], edi
		mov	[rsi+8], r14
		test	edi, edi
		jz	short loc_14000D47D
		mov	r8, rbx
		mov	r9d, edi
		sub	r8, rsi
		lea	rdx, [rsi+10h]

loc_14000D448:				; CODE XREF: sub_14000D36C+10Fj
		mov	rax, [r8+rdx-10h]
		shr	rax, 0Ch
		mov	[rdx], rax
		mov	eax, 0
		mov	rcx, [r8+rdx-8]
		lea	rdx, [rdx+10h]
		test	rcx, 0FFFh
		setnz	al
		sar	rcx, 0Ch
		add	rax, rcx
		mov	[rdx-8], rax
		sub	r9, 1
		jnz	short loc_14000D448

loc_14000D47D:				; CODE XREF: sub_14000D36C+CDj
		mov	edx, 68506D4Dh	; Tag
		mov	rcx, rbx	; P
		call	cs:ExFreePoolWithTag
		xor	eax, eax
		mov	cs:P, rsi
		jmp	loc_14000D3E5
sub_14000D36C	endp

; ---------------------------------------------------------------------------
algn_14000D499:				; DATA XREF: .pdata:000000014000A504o
		align 4

; =============== S U B	R O U T	I N E =======================================


cookie_func1	proc near		; CODE XREF: DriverEntry+10p
		mov	rax, cs:__security_cookie
		xor	r9d, r9d
		mov	r8, 2B992DDFA232h
		test	rax, rax
		jz	short loc_14000D4BA
		cmp	rax, r8
		jnz	short loc_14000D4F2

loc_14000D4BA:				; CODE XREF: cookie_func1+17j
		rdtsc
		shl	rdx, 20h
		lea	rcx, __security_cookie
		or	rax, rdx
		xor	rax, rcx
		mov	cs:__security_cookie, rax
		mov	word ptr cs:__security_cookie+6, r9w
		mov	rax, cs:__security_cookie
		test	rax, rax
		jnz	short loc_14000D4F2
		mov	rax, r8
		mov	cs:__security_cookie, rax

loc_14000D4F2:				; CODE XREF: cookie_func1+1Cj
					; cookie_func1+4Aj
		not	rax
		mov	cs:BugCheckParameter3, rax
		retn
cookie_func1	endp

; ---------------------------------------------------------------------------
		align 20h
; const	WCHAR aMmallocatecont
aMmallocatecont:			; DATA XREF: set_func_and_page_table_pointers+1B5o
		unicode	0, <MmAllocateContiguousNodeMemory>,0
		align 20h
; const	WCHAR SourceString
SourceString:				; DATA XREF: set_func_and_page_table_pointers+6Ao
		unicode	0, <MmGetVirtualForPhysical>,0
__IMPORT_DESCRIPTOR_ntoskrnl_exe dd rva	off_14000D5D8 ;	Import Name Table
		dd 0			; Time stamp
		dd 0			; Forwarder Chain
		dd rva aNtoskrnl_exe	; DLL Name
		dd rva KeGetCurrentProcessorNumberEx ; Import Address Table
__IMPORT_DESCRIPTOR_WDFLDR_SYS dd rva off_14000D5B0 ; Import Name Table
		dd 0			; Time stamp
		dd 0			; Forwarder Chain
		dd rva aWdfldr_sys	; DLL Name
		dd rva __imp_WdfVersionBind ; Import Address Table
		dq 3 dup(0)
;
; Import names for WDFLDR.SYS
;
off_14000D5B0	dq rva word_14000D9EC	; DATA XREF: INIT:__IMPORT_DESCRIPTOR_WDFLDR_SYSo
		dq rva word_14000D9D8
		dq rva word_14000DA14
		dq rva word_14000D9FE
		dq 0
;
; Import names for ntoskrnl.exe
;
off_14000D5D8	dq rva word_14000D6F8	; DATA XREF: INIT:__IMPORT_DESCRIPTOR_ntoskrnl_exeo
		dq rva word_14000D718
		dq rva word_14000D730
		dq rva word_14000D744
		dq rva word_14000D75C
		dq rva word_14000D778
		dq rva word_14000D782
		dq rva word_14000D79A
		dq rva word_14000D7B2
		dq rva word_14000D7CA
		dq rva word_14000D7DA
		dq rva word_14000D7EE
		dq rva word_14000D810
		dq rva word_14000D834
		dq rva word_14000D854
		dq rva word_14000D874
		dq rva word_14000D894
		dq rva word_14000D8B2
		dq rva word_14000D8CC
		dq rva word_14000D8DC
		dq rva word_14000D8E8
		dq rva word_14000D904
		dq rva word_14000D91C
		dq rva word_14000D936
		dq rva word_14000D94C
		dq rva word_14000D962
		dq rva word_14000D972
		dq rva word_14000D988
		dq rva word_14000D998
		dq rva word_14000D9A2
		dq rva word_14000D9C0
		dq rva word_14000D6E0
		dq 0
word_14000D6E0	dw 7E0h			; DATA XREF: INIT:000000014000D6D0o
		db 'RtlInitUnicodeString',0
		align 8
word_14000D6F8	dw 403h			; DATA XREF: INIT:off_14000D5D8o
		db 'KeGetCurrentProcessorNumberEx',0
word_14000D718	dw 9Ah			; DATA XREF: INIT:000000014000D5E0o
		db 'ExAllocatePoolWithTag',0
word_14000D730	dw 0C1h			; DATA XREF: INIT:000000014000D5E8o
		db 'ExFreePoolWithTag',0
word_14000D744	dw 0ACh			; DATA XREF: INIT:000000014000D5F0o
		db 'ExDeleteResourceLite',0
		align 4
word_14000D75C	dw 507h			; DATA XREF: INIT:000000014000D5F8o
		db 'MmGetSystemRoutineAddress',0
word_14000D778	dw 9B9h			; DATA XREF: INIT:000000014000D600o
		db 'ZwClose',0
word_14000D782	dw 0A8Eh		; DATA XREF: INIT:000000014000D608o
		db 'ZwWaitForSingleObject',0
word_14000D79A	dw 3AAh			; DATA XREF: INIT:000000014000D610o
		db 'KdDebuggerNotPresent',0
		align 2
word_14000D7B2	dw 0A91h		; DATA XREF: INIT:000000014000D618o
		db '__C_specific_handler',0
		align 2
word_14000D7CA	dw 7D0h			; DATA XREF: INIT:000000014000D620o
		db 'RtlGetVersion',0
word_14000D7DA	dw 733h			; DATA XREF: INIT:000000014000D628o
		db 'RtlCompareMemory',0
		align 2
word_14000D7EE	dw 49Eh			; DATA XREF: INIT:000000014000D630o
		db 'KeSetSystemGroupAffinityThread',0
		align 10h
word_14000D810	dw 487h			; DATA XREF: INIT:000000014000D638o
		db 'KeRevertToUserGroupAffinityThread',0
word_14000D834	dw 442h			; DATA XREF: INIT:000000014000D640o
		db 'KeQueryActiveProcessorCountEx',0
word_14000D854	dw 408h			; DATA XREF: INIT:000000014000D648o
		db 'KeGetProcessorNumberFromIndex',0
word_14000D874	dw 51Bh			; DATA XREF: INIT:000000014000D650o
		db 'MmMapLockedPagesSpecifyCache',0
		align 4
word_14000D894	dw 4E1h			; DATA XREF: INIT:000000014000D658o
		db 'MmAllocateContiguousMemory',0
		align 2
word_14000D8B2	dw 4FBh			; DATA XREF: INIT:000000014000D660o
		db 'MmFreeContiguousMemory',0
		align 4
word_14000D8CC	dw 26Ch			; DATA XREF: INIT:000000014000D668o
		db 'IoAllocateMdl',0
word_14000D8DC	dw 2BFh			; DATA XREF: INIT:000000014000D670o
		db 'IoFreeMdl',0
word_14000D8E8	dw 504h			; DATA XREF: INIT:000000014000D678o
		db 'MmGetPhysicalMemoryRanges',0
word_14000D904	dw 503h			; DATA XREF: INIT:000000014000D680o
		db 'MmGetPhysicalAddress',0
		align 4
word_14000D91C	dw 508h			; DATA XREF: INIT:000000014000D688o
		db 'MmGetVirtualForPhysical',0
word_14000D936	dw 53Bh			; DATA XREF: INIT:000000014000D690o
		db 'MmSystemRangeStart',0
		align 4
word_14000D94C	dw 7E3h			; DATA XREF: INIT:000000014000D698o
		db 'RtlInitializeBitMap',0
word_14000D962	dw 72Eh			; DATA XREF: INIT:000000014000D6A0o
		db 'RtlClearBits',0
		align 2
word_14000D972	dw 52Dh			; DATA XREF: INIT:000000014000D6A8o
		db 'MmProbeAndLockPages',0
word_14000D988	dw 53Fh			; DATA XREF: INIT:000000014000D6B0o
		db 'MmUnlockPages',0
word_14000D998	dw 0AEDh		; DATA XREF: INIT:000000014000D6B8o
		db 'strcmp',0
		align 2
word_14000D9A2	dw 3D4h			; DATA XREF: INIT:000000014000D6C0o
		db 'KeBugCheckEx',0
		align 2
aNtoskrnl_exe	db 'ntoskrnl.exe',0     ; DATA XREF: INIT:000000014000D57Co
		align 20h
word_14000D9C0	dw 746h			; DATA XREF: INIT:000000014000D6C8o
		db 'RtlCopyUnicodeString',0
		align 8
word_14000D9D8	dw 8			; DATA XREF: INIT:000000014000D5B8o
		db 'WdfVersionUnbind',0
		align 4
word_14000D9EC	dw 6			; DATA XREF: INIT:off_14000D5B0o
		db 'WdfVersionBind',0
		align 2
word_14000D9FE	dw 7			; DATA XREF: INIT:000000014000D5C8o
		db 'WdfVersionBindClass',0
word_14000DA14	dw 9			; DATA XREF: INIT:000000014000D5C0o
		db 'WdfVersionUnbindClass',0
aWdfldr_sys	db 'WDFLDR.SYS',0       ; DATA XREF: INIT:000000014000D590o
		align 200h
		dq 80h dup(?)
INIT		ends


		end DriverEntry
