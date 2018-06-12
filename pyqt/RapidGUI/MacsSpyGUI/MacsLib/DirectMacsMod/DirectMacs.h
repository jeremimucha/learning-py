
        /*################################################################*/
        /*################################################################*/
        /*####                                                        ####*/
        /*####       EHP Italy S.p.A. (CTI Software Development)      ####*/
        /*####                                                        ####*/
        /*################################################################*/
        /*####                                                        ####*/
        /*####  Direct Macs COMMUNICATION LIBRARY                     ####*/
        /*####                                                        ####*/
        /*####  Direct Macs file (DirectMacs.h)                       ####*/
        /*####                                                        ####*/
        /*####  This file contains all the declarations needed by the ####*/
        /*####  external applications for using the Direct Macs com-  ####*/
        /*####  munication beetween the PC and the Appliance Mini     ####*/
        /*####  Interface (AMI) & the Appliance eXtended Interface    ####*/
        /*####  (AXI)                                                 ####*/
        /*################################################################*/
        /*####                                                        ####*/
        /*####  Activity       : HDE250                               ####*/
        /*####                                                        ####*/
        /*####  Product        : Direct Macs Communication Library    ####*/
        /*####                                                        ####*/
        /*####  Version        : 1.23 (Microsoft Visual Studio 2005)  ####*/
        /*####                                                        ####*/
        /*####  Date           : 23/09/2008                           ####*/
        /*####                                                        ####*/
        /*####  Programmer     : Alessio Mattè & Giovanni Dal Bello   ####*/
        /*####                                                        ####*/
        /*####  Notes          :                                      ####*/
        /*####                                                        ####*/
        /*################################################################*/
        /*################################################################*/


/***********************************************/
/* Skip all if this file has been already read */
/***********************************************/
#ifndef DIRECTMACS_H
#define DIRECTMACS_H


/* If C++ prevent name mangling */
/* ============================ */
#ifdef __cplusplus
    extern "C" {
#endif


/* Target operating system: one of the "windows" family? */
/* ===================================================== */
#ifdef _Windows

/* Define the __WINDOWS__ macro if necessary */
#ifndef __WINDOWS__
#define __WINDOWS__
#endif

#endif

/* Target operating system: one of the "windows 32-bit" family? */
/* ============================================================ */
#ifdef __WIN32__

/* Define the __WINDOWS__ macro if necessary */
#ifndef __WINDOWS__
#define __WINDOWS__
#endif

#endif

/* Target operating system: one of the "windows" family? (LabWindows/CVI only) */
/* =========================================================================== */
#ifdef _CVI_

/* Define the __WINDOWS__ macro if necessary */
#ifndef __WINDOWS__
#define __WINDOWS__
#endif

#endif


/* Is Windows 32-bit the target operating system? */
/* ============================================== */
#ifdef __WIN32__

/* Microsoft Visual C++? */
#if defined(_MSC_VER)

// The following ifdef block is the standard way of creating macros which make exporting 
// from a DLL simpler. All files within this DLL are compiled with the DMACSAPI_EXPORTS
// symbol defined on the command line. this symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see 
// DMACSAPI_EXPORTS functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.

/* Define the DMACSAPI calling convention macro (Microsoft Visual C++) */
#ifdef DMACSAPI_EXPORTS
#define DMACSAPI __declspec(dllexport) __stdcall
#else
#define DMACSAPI __declspec(dllimport) __stdcall
#endif

#elif defined(__GNUC__)

#ifdef DMACSAPI_EXPORTS
#define DMACSAPI __declspec(dllexport) __stdcall
#else
#define DMACSAPI __declspec(dllimport) __stdcall
#endif

#else


/* Define the DMACSAPI calling convention macro (Borland C++, LabWindows/CVI) */
#ifdef DMACSAPI_EXPORTS
#define DMACSAPI __export __stdcall
#else
#define DMACSAPI __import __stdcall
#endif

#endif

#else

#error "The HACL Communication Library only supports Win32 operating systems"

#endif


#ifndef TYPE_INTERFACE_DEF
#define TYPE_INTERFACE_DEF

/* Define a signed 8-bit integer */
typedef signed char Int8;

/* Define an unsigned 8-bit integer */
typedef unsigned char uInt8;

/* Define a signed 16-bit integer */
typedef signed short int Int16;

/* Define an unsigned 16-bit integer */
typedef unsigned short int uInt16;

/* Define a signed 32-bit integer */
typedef signed long int Int32;

/* Define an unsigned 32-bit integer */
typedef unsigned long int uInt32;

#endif

/* Product identification macros */
#define PRODUCT_NAME    "Direct MACS Communication Library 1.23"
#define MAJOR_VERSION  ((uInt16) 1)
#define MINOR_VERSION  ((uInt16) 23)

/* Maximum length of the USB description string, including the terminatin null character */
#define MAX_USB_DESCR_LEN		100

/* Channels buffer size */
#define CHANNELS_BUFF_SIZE		127

/* No more than 127 devices can be connected to one USB bus */
#define DMACS_CHANNELS          CHANNELS_BUFF_SIZE


/* Function return codes */
#define DMACS_OK                        0   /* Success code */
#define DMACS_FAILURE                   1   /* Generic failure code */
#define DMACS_NOT_PERFORMED             2   /* Required operation not performed */
#define DMACS_INSUFFICIENT_RESOURCES    3   /* Insufficient hardware resources */
#define DMACS_CHANNEL_ALREADY_OPEN      4   /* The specified channel is already open */
#define DMACS_CHANNEL_ALREADY_CLOSE     5   /* The specified channel is already closed */
#define DMACS_CHANNEL_CLOSE             6   /* The specified channel is closed */
#define DMACS_CHANNEL_ERROR             7   /* A channel error occured */
#define DMACS_CHANNEL_NOT_AVAILABLE     8   /* The specified channel is not available */
#define DMACS_INVALID_PARAMETERS        9   /* The specified input parameters are invalid */

#define DMACS_SEND_CARRIER_ON			10	/* Carrier ON conflict. This error occurs when it is no possibile to send a */
											/* MACS message to the bus because in the meantime the application is */
											/* receiving another MACS message and so the bus is engaged */
#define DMACS_SEND_COLLISION			11  /* Collision detected on the bus. This error condition occurs when a MACS message */
											/* is sent to the bus and in the same time some other unit starts to communicate. */
											/* This error condition is noticed by the library because when a message is sent */
											/* to the bus, each sent byte is checked using the echo feature of MACS */
#define DMACS_SEND_ACK_ERROR			12	/* Acknowledge error. This error error condition occurs when a MACS message */
											/* is sent to the bus and the ACK message received does not match the message just */
											/* sent (the checksum in the body of the ACK is different from the checksum of the message) */
#define DMACS_SEND_TIMEOUT_EXPIRED_CHECK_COLLISION		13	/* Timeout expired checking the collision */
#define DMACS_SEND_TIMEOUT_EXPIRED_CHECK_ACK			14	/* Timeout expired checking the acknowledge. In the MACS bus after the */
															/* reception of a message, the target unit must generate an acknowledge. */
															/* It must start transmitting such acknowledge not before 5ms and complete */
															/* it within 19ms after the end of the message just received. If the acknowledge */
															/* is not received by the source unit within this time interval, this error */
															/* condition occurs */

#define DMACS_MESSAGE_RECEIVING         15  /* A message is under reception */
#define DMACS_NO_MESSAGE_RECEIVED       16  /* No messages received from the MACS bus */
#define DMACS_MESSAGE_TIMEOUT			17	/* Timeout expired during the reception of a MACS message */
#define DMACS_MESSAGE_BAD_LENGTH		18	/* The MACS message received is characterized by a bad length */
#define DMACS_MESSAGE_BAD_CHECKSUM		19	/* The MACS message received is characterized by a bad checksum */
#define DMACS_GET_MESSAGE_ERROR         20  /* A generic error occured while retrieving a message from the MACS bus */
#define DMACS_MESSAGE_RECEIVED          21  /* Message received from the MACS bus */

#define DMACS_NO_CONNECTION             22  /* No connection: no device sent the configuration request message */
#define DMACS_CONNECTION_ERROR          23  /* Connection error: error condition detected */
#define DMACS_CONNECTION_OK             24  /* Connection OK: a device sent the configuration request message */

#define DMACS_SETUP_CHANNEL_OPEN        25  /* The channel specified during the test phase is open */
#define DMACS_SETUP_CHANNEL_CLOSE       26  /* The channel specified during the test phase is closed */
#define DMACS_NOT_SETUP                 27  /* Direct Macs communication not yet setup */

#define DMACS_FTD2XX_DLL_NOT_FOUND      28  /* FTD2XX.dll dynamic library not found */
#define DMACS_DRIVER_NOT_FOUND          29  /* Electrolux's drivers not found (ELUXBUS.sys/ELUXSER.sys/MACS.sys) */

#define DMACS_QUEUE_RECEIVED			30  /* The content of the parallel queue has been received */
#define DMACS_QUEUE_EMPTY				31  /* The parallel queue is empty */
#define DMACS_QUEUE_OVERRUN				32  /* An overrun condition has been verified on the parallel queue */
#define DMACS_QUEUE_ERROR				33  /* A generic error occured while retrieving the messages contained inside the parallel queue */


/* Maximum limits macros */
#define MAX_ID_STRING_LEN               8
#define MAX_VAR_NR                      16
#define MAX_VAR_SIZE                    15

/* Maximum MACS message length */
#define MAX_MACS_INFO_LEN               40

/* Maximum MACS message length */
#define MAX_MACS_MESSAGE_LENGTH = MAX_MACS_INFO_LEN + 5; // 1 byte of HEADER
														 // 1 byte of DESTINATION ADDRES
														 // 1 byte of SOURCE ADDRESS
														 // 1 byte of LENGTH
														 // "MAX_MACS_INFO_LEN" bytes of PAYLOAD
														 // 1 byte of CHECKSUM

/* Message silence time (ms) */
#define MESSAGE_SILENCE_TIME           100

/* Minimum receiver queue length (number of MACS messages) */
#define MIN_RECEIVER_QUEUE_LENGTH		10

/* Minimum ACK generation delay (ms) */
#define MINIMUM_ACK_DELAY				6

/* Default initial receive timeout value for MACS request messages (ms) */
/* This parameter influences the behavior of the MACS Upper Filter Driver	*/
/* It is possible adjust this parameter using the "SetKernelTiming" function (see below), but this function is */
/* intended for advanced users */
#define DEFAULT_INITIAL_REQ_REC_TIMEOUT		60

/* Default receive timeout value for MACS acknowledge messages (ms) */
/* This parameter influences the behavior of the MACS Upper Filter Driver */
/* It is possible adjust this parameter using the "SetKernelTiming" function (see below), but this function is */
/* intended for advanced users */
#define DEFAULT_ACK_REC_TIMEOUT				20


// RX parallel queue states definition
enum RxParallelQueueItemState { 
	RC_UNUSED_ELEMENT,    // Free queue element
	RC_RX_MSG_REC,        // Receiving message
	RC_RX_MSG_RIGHT,      // Message properly received
	RC_RX_BAD_CHAR,       // Bad character received
	RC_RX_BAD_LENGTH,     // Bad length received
	RC_RX_BAD_CHECKSUM,   // Bad checksum received
	RC_RX_MSG_TIMEOUT,    // Timeout during the message reception
};

// Struct of a MACS message
struct MACSMessage {
	uInt8 Header;
	uInt8 LDU;
	uInt8 LSU;
	uInt8 Length;
	uInt8 Body[45]; 
	uInt8 Checksum;
	RxParallelQueueItemState Status;
	double Message_Time;
};


/****************************************************************************/
/*                           GetDMacsLibraryVersion                         */
/****************************************************************************/
/* TASK: this function yields the current version of the communication library */
/* PARAMETERS: pui16MajorVersion -> yields the major release number (if not NULL) */
/*             pui16MinorVersion -> yields the minor release number (if not NULL) */
/* RETURNS: nothing */
/* NOTES: none */
void DMACSAPI GetDMacsLibraryVersion (uInt16 * pui16MajorVersion, uInt16 * pui16MinorVersion);


/****************************************************************************/
/*                           DMacsSupportTest                               */
/****************************************************************************/
/* TASK: this function tests if driver and required DLL for Direct Macs connection have been installed in the host PC */
/* PARAMETERS: none */
/* RETURNS: DMACS_OK if system supports DIRECT MACS communication (FTC2232C/FT232B driver and library are present) */
/*          DMACS_FTD2XX_DLL_NOT_FOUND if FTD2XX.dll not found */
/*          DMACS_DRIVER_NOT_FOUND if the USB driver for interface module is not installed in Windows */
/* NOTES: none */
uInt32 DMACSAPI DMacsSupportTest (void);


/****************************************************************************/
/*                        DMacsSetupTest                                    */
/****************************************************************************/
/* TASK: this function tests whether the Direct Macs communication is setup for the specified channel */
/* PARAMETERS: i16ChannelNr -> the communication channel */
/* RETURNS: DMACS_SETUP_CHANNEL_OPEN, if Direct Macs OK ("SetupDMacsCom" already called) and the specified channel is open */
/*          DMACS_SETUP_CHANNEL_CLOSE, if the specified channel is closed */
/*          DMACS_NOT_SETUP, if Direct Macs not yet setup */
/*          DMACS_CHANNEL_NOT_AVAILABLE, if the specified channel is not available */
/* NOTES: none */
uInt32 DMACSAPI DMacsSetupTest (Int16 i16ChannelNr);


/****************************************************************************/
/*                        DMacsGetAvailableChannels                         */
/****************************************************************************/
/* TASK: this function yields the list of the available channels for Direct Macs */
/* PARAMETERS: pui8Count                                --> number of available channels (pointer to 8 bit unsigned integer) */
/*             char szDescriptions[][MAX_USB_DESCR_LEN] --> array of channel names (array of null */
/*                                                          terminated strings of MAX_USB_DESCR_LEN chars) */
/*             uInt32 pui32LocIDs[]                     --> array of location IDs (array of unsigned 32-bit integers) */
/* RETURNS: DMACS_OK: channels identified successfully or no available channels */
/*          DMACS_CHANNEL_ERROR: some errors happened quering FTDI devices */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: this function yields DMACS_OK also if no channels have been detected. */
/*        This function does not list channels you have already opened with 'SetupDMacsCom' function or */
/*        opened by other programs in the system  */
/*        The maximum number of supported channels is DMACS_CHANNELS. */
/* NOTES: none */
uInt32 DMACSAPI DMacsGetAvailableChannels (uInt8 * pui8Count, char szDescriptions[][MAX_USB_DESCR_LEN],
                                           uInt32 pui32LocIDs[]);


/****************************************************************************/
/*                        SetupDMacsCom                                     */
/****************************************************************************/
/* TASK: this function initializes the communication, by opening the specified channel, and */
/*       by setting the receiver queue dimension */
/* PARAMETERS: szDescription     -> name of the channel to open, as returned by DMacsGetAvailableChannels (null terminated string) */
/*             ui32LocID         -> location ID of the channel to open, as returned by DMacsGetAvailableChannels (unsigned 32 bit integer) */
/*             ui16RxQueueLength -> length of the receiver queue (it should be greater or equal than MIN_RECEIVER_QUEUE_LENGTH and less than 65536) */ 
/*             pi16ChannelNr     -> yields the channel number for the successfully opened channel, to be used */
/*                                  for all subsequent calls to this channel (it must be not NULL) */
/* RETURNS: DMACS_OK if success */
/*          DMACS_INSUFFICIENT_RESOURCES if the system resources are insufficient to execute the operation */
/*          DMACS_CHANNEL_ALREADY_OPEN if the specified channel is already open */
/*          DMACS_FAILURE if an error occurred */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: none */
uInt32 DMACSAPI SetupDMacsCom (const char szDescription[], uInt32 ui32LocID,
                               uInt16 ui16RxQueueLength, Int16 * pi16ChannelNr);


/****************************************************************************/
/*                          ResetDMacsCom                                   */
/****************************************************************************/
/* TASK: this function ends the communication */
/* PARAMETERS: i16ChannelNr -> the communication channel */
/* RETURNS: DMACS_OK if success */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_CHANNEL_ALREADY_CLOSE if the specified channel is already closed */
/*          DMACS_FAILURE if an error occurred */
/* NOTES: none */
uInt32 DMACSAPI ResetDMacsCom (Int16 i16ChannelNr);


/****************************************************************************/
/*                           SetKernelTiming                                */
/****************************************************************************/
/* TASK: this function sets the timing of the MACS Upper Filter Driver */
/* PARAMETERS: i16ChannelNr    -> the communication channel */
/*             ui16AckDelay    -> the time to wait before generating the acknowledge message (6..65535) (in ms). */
/*             ui16InitialReqRecTimeout	-> the initial receive timeout value for MACS request messages */
/*										   The MACS Upper Filter driver works well for values equal or greater */
/*										   than 15 ms (60 ms is the default value) */
/*             ui16AckRecTimeout		-> the receive timeout value for MACS acknowledge messages */
/*										   The MACS Upper Filter driver works well for values equal or greater */
/*                                         than 1 ms (20 ms is the default value) */
/* RETURNS: DMACS_OK if success */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/*          DMACS_FAILURE if an error occurred */
/* NOTES: this function should be used by advanced users only */
uInt32 DMACSAPI SetKernelTiming (Int16 i16ChannelNr, uInt16 ui16AckDelay, 
								 uInt16 ui16InitialReqRecTimeout, uInt16 ui16AckRecTimeout);


/****************************************************************************/
/*                              GetKernelTiming                             */
/****************************************************************************/
/* TASK: this function gets the timing of the MACS Upper Filter Driver */
/* PARAMETERS: i16ChannelNr     -> the communication channel (0=FTDI channel 1, 1=FTDI channel 2, etc...) */
/*             pui16AckDelay    -> if not NULL, yields the time to wait before generating the acknowledge messages (in ms) */
/*             pui16InitialReqRecTimeout -> if not NULL, yields the initial receive timeout value for MACS request */
/*                                          messages (in ms) */
/*             pui16AckRecTimeout		 -> if not NULL, yields the receive timeout value for MACS acknowledge */
/*                                          messages (in ms) */
/* RETURNS: DMACS_OK if success */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_FAILURE if an error occurred */
/* NOTES: this function should be used by advanced users only */
uInt32 DMACSAPI GetKernelTiming (Int16 i16ChannelNr, uInt16 * pui16AckDelay,
								 uInt16 * pui16InitialReqRecTimeout, uInt16 * pui16AckRecTimeout);


/****************************************************************************/
/*                           SetMacsAddress                                 */
/****************************************************************************/
/* TASK: this function assigns a MACS address to the Command Module */
/* PARAMETERS: i16ChannelNr    -> the communication channel */
/*             ui8UnitCode     -> unit code (0..31)  */
/*                                The unit code represents the 5 least significant bits in the address byte */
/*             ui8UnitDistCode -> distinctive code of the unit (0..7) */
/*                                The distinctive code represents the 3 most significant bits in the address byte */
/* RETURNS: DMACS_OK if success */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/*          DMACS_FAILURE if an error occurred */
/* NOTES: whenever you open the communication with 'SetupDMacsCom', the library assigns the following */
/*        default MACS address to the Command Module: ui8UnitCode=0x1E, ui8UnitDistCode=0x01.  */
/*        As a consequence, the default complete MACS address of the Command Module is 0x3E. */
/*		  The default values assigned to the time to wait before generating the acknowledge message, */
/*        the initial receive timeout for MACS request messages and the receive timeout. */
/*        for MACS acknowledge messages are respectively 6 ms, 60 ms and 20 ms */
/* NOTES: calling this function has the same effect as calling SetMacsAddress_Ex */
/*        with ui8TabUnitPos = 0 */
uInt32 DMACSAPI SetMacsAddress (Int16 i16ChannelNr, uInt8 ui8UnitCode, uInt8 ui8UnitDistCode);


/****************************************************************************/
/*                         SetMacsAddressEx                                 */
/****************************************************************************/
/* TASK: this function assigns a MACS address to the Command Module and allows to specify the internal */
/*       MACS table index of this address. Up to five different MACS addresses can be assigned simultaneously */
/*       to the Command Module */
/* PARAMETERS: i16ChannelNr    -> the communication channel */
/*             ui8TabUnitPos   -> index to internal MACS address table item (0..4) */
/*             ui8UnitCode     -> unit code (0..31)  */
/*                                The unit code represents the 5 least significant bits in the address byte */
/*             ui8UnitDistCode -> distinctive code of the unit (0..7) */
/*                                The distinctive code represents the 3 most significant bits in the address byte */
/* RETURNS: DMACS_OK if success */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/*          DMACS_FAILURE if an error occurred */
/* NOTES: whenever you open the communication with 'SetupDMacsCom', the library assigns the following */
/*        default MACS address to the Command Module: ui8UnitCode=0x1E, ui8UnitDistCode=0x01.  */
/*        As a consequence, the default complete MACS address of the Command Module is 0x3E. */
/*		  The default values assigned to the time to wait before generating the acknowledge message, */
/*        the initial receive timeout for MACS request messages and the receive timeout */
/*        for MACS acknowledge messages are respectively 6 ms, 60 ms and 20 ms */
uInt32 DMACSAPI SetMacsAddressEx (Int16 i16ChannelNr, uInt8 ui8TabUnitPos, uInt8 ui8UnitCode, uInt8 ui8UnitDistCode);


/****************************************************************************/
/*                               GetMacsAddress                             */
/****************************************************************************/
/* TASK: this function gets the MACS address of the Command Module.  */
/* PARAMETERS: i16ChannelNr     -> the communication channel (0=FTDI channel 1, 1=FTDI channel 2, etc...) */
/*             pui8UnitCode     -> yields the unit code (if not NULL) */
/*                                 The unit code represents the 5 least significant bits in the address byte. */
/*             pui8UnitDistCode -> yields the distinctive code of the unit (if not NULL) */
/*                                 The distinctive code represents the 3 most significant bits in the address byte. */
/* RETURNS: DMACS_OK if success */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_FAILURE if an error occurred */
/* NOTES: calling this function has the same effect as calling GetMacsAddress_Ex */
/*        with ui8TabUnitPos = 0 */
uInt32 DMACSAPI GetMacsAddress (Int16 i16ChannelNr, uInt8 * pui8UnitCode, uInt8 * pui8UnitDistCode);


/****************************************************************************/
/*                             GetMacsAddressEx                             */
/****************************************************************************/
/* TASK: this function gets the MACS address of the Command Module based on the internal MACS table index */
/*       passed to the function */
/* PARAMETERS: i16ChannelNr     -> the communication channel (0=FTDI channel 1, 1=FTDI channel 2, etc...) */
/*             ui8TabUnitPos    -> index to internal MACS address table item (0..4) */
/*             pui8UnitCode     -> yields the unit code (if not NULL) */
/*                                 The unit code represents the 5 least significant bits in the address byte. */
/*             pui8UnitDistCode -> yields the distinctive code of the unit (if not NULL) */
/*                                 The distinctive code represents the 3 most significant bits in the address byte. */
/* RETURNS: DMACS_OK if success */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_FAILURE if an error occurred */
/* NOTES: none */
uInt32 DMACSAPI GetMacsAddressEx (Int16 i16ChannelNr, uInt8 ui8TabUnitPos, uInt8 * pui8UnitCode, uInt8 * pui8UnitDistCode);


/****************************************************************************/
/*                           SendMacsMessage                                */
/****************************************************************************/
/* TASK: this function sends a "MACS massage" to the bus */
/* PARAMETERS: i16ChannelNr  -> the communication channel */
/*             ui8LDU        -> the logical destination unit */
/*             ui8LSU        -> the logical source unit */
/*             ui8MacsMsgLen -> the length of the MACS message (1..MAX_MACS_INFO_LEN) */
/*             pui8MacsMsg[] -> the MACS message */
/*             ui16Attempts  -> maximum number of attempts to send the message */
/*             pui8Checksum  -> if not NULL, it yields the checksum of the sent message */
/* RETURNS: DMACS_OK if the MACS message has been correctly sent to the bus */
/*          DMACS_SEND_CARRIER_ON if it is no possible to send a MACS message to the bus because in the */
/*                                meantime the application is receiving another MACS message and so the */
/*                                bus is engaged */
/*          DMACS_SEND_COLLISION if a collision situation has been detected on the bus. This error condition */
/*                               occurs when a MACS message is sent to the bus and at the same time some other */
/*                               unit starts to communicate. This error condition is noticed by the library */
/*                               because when a message is sent to the bus, each sent byte is checked using the echo */
/*                               feature of MACS */
/*          DMACS_SEND_ACK_ERROR if the ACK message received does not match the message just sent (the checksum in the body */
/*                               of the ACK is different from the checksum of the message) */
/*          DMACS_SEND_TIMEOUT_EXPIRED_CHECK_COLLISION if timeout expired checking collision */
/*          DMACS_SEND_TIMEOUT_EXPIRED_CHECK_ACK if timeout expired checking acknowledge. In the MACS bus after */
/*                                               the reception of a message, the target unit must generate an acknowledge. */
/*                                               It must start transmitting such acknowledge not before 5ms and complete it */
/*                                               within 19ms after the end of the message just received. If the acknowledge */
/*                                               is not received by the source unit within this time interval, this error */
/*                                               condition occurs */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/*          DMACS_FAILURE if an error occurred during the dispatch of the MACS message. Usually */
/*                        this error is due to a low-level problem on the FTDI chip */
/* NOTES: none */
uInt32 DMACSAPI SendMacsMessage (Int16 i16ChannelNr, uInt8 ui8LDU, uInt8 ui8LSU,
                                 uInt8 ui8MacsMsgLen, const uInt8 pui8MacsMsg [], 
								 uInt16 ui16Attempts, uInt8 * pui8Checksum);


/****************************************************************************/
/*                           GetMacsMessage                                 */
/****************************************************************************/
/* TASK: this function reads the "MACS massages" coming from the bus */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui16SleepTime      -> the sleep time before reading the input queue (in ms) */
/*             pui8LDU            -> yields the logical destination unit (if not NULL) */
/*             pui8LSU            -> yields the logical source unit (if not NULL) */
/*             pui8MacsMsgLen     -> yields the length of the MACS message (if not NULL) */
/*             pui8MacsMsg        -> yields the MACS message:the body (if not NULL) */
/*             pdMacsMsgTimeStamp -> yields the time stamp of the received message in seconds (if not NULL) */
/* RETURNS: DMACS_MESSAGE_RECEIVED if a message has been received */
/*          DMACS_MESSAGE_RECEIVING if a message is under reception */
/*          DMACS_NO_MESSAGE_RECEIVED if no messages have been received */
/*          DMACS_MESSAGE_TIMEOUT if timeout expired during the reception of the message */
/*          DMACS_MESSAGE_BAD_LENGTH if the received message is characterized by a bad length */
/*          DMACS_MESSAGE_BAD_CHECKSUM if the received message is characterized by a bad checksum */
/*          DMACS_GET_MESSAGE_ERROR if error condition detected */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/* NOTES: none */
uInt32 DMACSAPI GetMacsMessage (Int16 i16ChannelNr,	uInt16 ui16SleepTime,
								uInt8 * pui8LDU, uInt8 * pui8LSU,
								uInt8 * pui8MacsMsgLen, uInt8 pui8MacsMsg [],
								double * pdMacsMsgTimeStamp);


/****************************************************************************/
/*                          GetMacsMessageEx                                */
/****************************************************************************/
/* TASK: this function reads the "MACS massages" coming from the bus and gives more */
/*		 functionalities respect the "GetMacsMessage" function */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui16SleepTime      -> the sleep time before reading the input queue (in ms) */
/*             pui8HDR            -> yields the header (if not NULL) */
/*             pui8LDU            -> yields the logical destination unit (if not NULL) */
/*             pui8LSU            -> yields the logical source unit (if not NULL) */
/*             pui8MacsMsgLen     -> yields the length of the MACS message (if not NULL) */
/*             pui8MacsMsg        -> yields the MACS message: the body (if not NULL) */
/*             pui8CHK			  -> yields the checksum (if not NULL) */
/*             pdMacsMsgTimeStamp -> yields the time stamp of the received message in seconds (if not NULL) */
/* RETURNS: DMACS_MESSAGE_RECEIVED if a message has been received */
/*          DMACS_MESSAGE_RECEIVING if a message is under reception */
/*          DMACS_NO_MESSAGE_RECEIVED if no messages have been received */
/*          DMACS_MESSAGE_TIMEOUT if timeout expired during the reception of the message */
/*          DMACS_MESSAGE_BAD_LENGTH if the received message is characterized by a bad length */
/*          DMACS_MESSAGE_BAD_CHECKSUM if the received message is characterized by a bad checksum */
/*          DMACS_GET_MESSAGE_ERROR if error condition detected */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/* NOTES: none */
uInt32 DMACSAPI GetMacsMessageEx (Int16 i16ChannelNr,	uInt16 ui16SleepTime,
								  uInt8 * pui8HDR, uInt8 * pui8LDU, uInt8 * pui8LSU,
								  uInt8 * pui8MacsMsgLen, uInt8 pui8MacsMsg [],
								  uInt8 * pui8CHK, double * pdMacsMsgTimeStamp);


/****************************************************************************/
/*                        GetMacsMessagesQueue                              */
/****************************************************************************/
/* TASK: this function reads all the "MACS messages" coming from the bus stored inside the parallel queue. The parallel */
/*       queue is used to sniff all messages in the MACS bus, without changing the functional behavior of the system */
/* PARAMETERS: i16ChannelNr         -> the communication channel */
/*             pmacsMsgs            -> yields the array containing the received messages (if not NULL). To avoid */
/*                                     any problems create an array with 65536 elements */
/*             pusNumberOfReadMsgs  -> yields the number of read messages (if not NULL) */
/*             pusNumberOfLostMsgs  -> yields the number of lost messages due to an overrun condition (if not NULL) */
/* RETURNS: DMACS_QUEUE_RECEIVED if a set of messages has been received */
/*          DMACS_QUEUE_EMPTY if the parallel queue does not contain any messages */
/*          DMACS_QUEUE_OVERRUN if an overrun condition has been verified: some MACS messages have been lost */
/*          DMACS_QUEUE_ERROR if a generic error occured while retrieving the messages contained inside the parallel queue */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/* NOTES: the length of the parallel queue is the same as the receiver queue (the value is set using the "SetupDMacsCom") */
/*        function) */
uInt32 DMACSAPI GetMacsMessagesQueue (Int16 i16ChannelNr,
									  MACSMessage pmacsMsgs [], 
									  uInt16 * pusNumberOfReadMsgs,
									  uInt16 * pusNumberOfLostMsgs);


/****************************************************************************/
/*                      GetMacsMessagesQueueLV                              */
/****************************************************************************/
/* TASK: this function reads all the "MACS messages" coming from the bus stored inside the parallel queue. The */
/*       parallel queue is used to sniff all messages in the MACS bus, without changing the functional behavior  */
/*       of the system. This function is the "GetMacsMessagesQueue" version for LabVIEW. A particular function for */
/*       LabVIEW is necessary because the "MACSMessage" structure cannot be interpreted correctly by LabVIEW: */
/*       each "MACSMessage" record is "translated" in a sequence of 59 bytes with this meaning : */
/*       Header       --> 1 byte */
/*       LDU          --> 1 byte */
/*       LSU          --> 1 byte */
/*       Length       --> 1 byte */
/*       Body         --> a sequence of 45 bytes */
/*       Checksum     --> 1 byte */
/*       Status       --> 1 byte */
/*       Message_Time --> 8 bytes. This value is expressed in ms. The byte with index 51 is the MSB, while the byte with */
/*                        index 58 is the LSB */
/* PARAMETERS: i16ChannelNr         -> the communication channel */
/*             pmacsMsgs            -> yields the 2-dimensions array containing the received messages (if not NULL). */
/*                                     Each array item is a flattened representation of a "MACS message" structure that */
/*                                     consists in a sequence of 59 bytes */
/*             pusNumberOfReadMsgs  -> yields the number of read messages (if not NULL) */
/*             pusNumberOfLostMsgs  -> yields the number of lost messages due to an overrun condition (if not NULL) */
/* RETURNS: DMACS_QUEUE_RECEIVED if a set of messages has been received */
/*          DMACS_QUEUE_EMPTY if the parallel queue does not contain any messages */
/*          DMACS_QUEUE_OVERRUN if an overrun condition has been verified: some MACS messages have been lost */
/*          DMACS_QUEUE_ERROR if a generic error occured while retrieving the messages contained inside the parallel queue */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/* NOTES: the length of the parallel queue is the same as the receiver queue (the value is set using the "SetupDMacsCom") */
/*        function) */
uInt32 DMACSAPI GetMacsMessagesQueueLV (Int16 i16ChannelNr,
										uInt8 pmacsMsgs [][59], 
										uInt16 * pusNumberOfReadMsgs,
										uInt16 * pusNumberOfLostMsgs);


/****************************************************************************/
/*                           DMacsMachineConnection                         */
/****************************************************************************/
/* TASK: MACSII DAAS 'machine connection' service */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui8LDU             -> the logical destination unit */
/*             ui8LSU             -> the logical source unit */
/*             ui16ReplyTimeout   -> the destination unit reply timeout (in ms) */
/*             ui16MinSilenceTime -> the minimum time interval between consecutive commands (in ms) */
/*             pui8IDString       -> yields the firmware's identification string (if not NULL) */
/* RETURNS: DMACS_CONNECTION_OK if a device sent the configuration request message */
/*          DMACS_NO_CONNECTION if no device sent the configuration request message */
/*          DMACS_CONNECTION_ERROR if error condition detected */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: "pui8IDString" must refer to a data buffer of at least (MAX_ID_STRING_LEN+1) bytes */
uInt32 DMACSAPI DMacsMachineConnection (Int16 i16ChannelNr, uInt8 ui8LDU, uInt8 ui8LSU,
                                        uInt16 ui16ReplyTimeout, uInt16 ui16MinSilenceTime, 
										uInt8 pui8IDString[]);


/****************************************************************************/
/*                           DMacsMemoryRead                                */
/****************************************************************************/
/* TASK: MACSII DAAS 'memory read' service */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui8LDU             -> the logical destination unit */
/*             ui8LSU             -> the logical source unit */
/*             ui16ReplyTimeout   -> the destination unit reply timeout (in ms) */
/*             ui16MinSilenceTime -> the minimum time interval between consecutive commands (in ms) */
/*             ui16MemAddress     -> the address of the first memory location */
/*             ui8Size            -> the size of the memory block */
/*             pui8Buffer         -> the target data buffer (it should be not NULL)*/
/* RETURNS: DMACS_OK if success */
/*          DMACS_FAILURE if an error occurred */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: none */
uInt32 DMACSAPI DMacsMemoryRead (Int16 i16ChannelNr, uInt8 ui8LDU, uInt8 ui8LSU,
                                 uInt16 ui16ReplyTimeout, uInt16 ui16MinSilenceTime,
								 uInt16 ui16MemAddress, uInt8 ui8Size, uInt8 pui8Buffer[]);


/****************************************************************************/
/*                           DMacsMemoryWrite                               */
/****************************************************************************/
/* TASK: MACSII DAAS 'memory write' service */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui8LDU             -> the logical destination unit */
/*             ui8LSU             -> the logical source unit */
/*             ui16ReplyTimeout   -> the destination unit reply timeout (in ms) */
/*             ui16MinSilenceTime -> the minimum time interval between consecutive commands (in ms) */
/*             ui16MemAddress     -> the address of the first memory location */
/*             ui8Size            -> the size of the memory block */
/*             pui8Buffer         -> the source data buffer */
/* RETURNS: DMACS_OK if success */
/*          DMACS_NOT_PERFORMED if operation not performed */
/*          DMACS_FAILURE if an error occurred */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: level 1 and 2 only */
uInt32 DMACSAPI DMacsMemoryWrite (Int16 i16ChannelNr, uInt8 ui8LDU, uInt8 ui8LSU,
                                  uInt16 ui16ReplyTimeout, uInt16 ui16MinSilenceTime, 
								  uInt16 ui16MemAddress, uInt8 ui8Size, const uInt8 pui8Buffer[]);


/****************************************************************************/
/*                           DMacsDetectMaxReadBlockSize                    */
/****************************************************************************/
/* TASK: this function sends a sequence of memory read commands to detect */
/*       the maximum size of the memory block readable with one command */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui8LDU             -> the logical destination unit */
/*             ui8LSU             -> the logical source unit */
/*             ui16ReplyTimeout   -> the destination unit reply timeout (in ms) */
/*             ui16MinSilenceTime -> the minimum time interval between consecutive commands (in ms) */
/*             ui16MemAddress     -> the address of the memory location for the */
/*                                   dummy read commands */
/*             pui8Size           -> yields the maximum size of the read memory block (in bytes) (it must be not NULL)*/
/* RETURNS: DMACS_OK if success */
/*          DMACS_FAILURE if an error occurred */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: none */
uInt32 DMACSAPI DMacsDetectMaxReadBlockSize (Int16 i16ChannelNr, uInt8 ui8LDU, uInt8 ui8LSU,
                                             uInt16 ui16ReplyTimeout, uInt16 ui16MinSilenceTime, 
											 uInt16 ui16MemAddress,  uInt8 * pui8Size);


/****************************************************************************/
/*                           DMacsDetectMaxWriteBlockSize                   */
/****************************************************************************/
/* TASK: this function sends a sequence of memory read commands to detect */
/*       the maximum size of the memory block writable with one command */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui8LDU             -> the logical destination unit */
/*             ui8LSU             -> the logical source unit */
/*             ui16ReplyTimeout   -> the destination unit reply timeout (in ms) */
/*             ui16MinSilenceTime -> the minimum time interval between consecutive commands (in ms) */
/*             ui16MemAddress     -> the address of the memory location for the */
/*                                   dummy read commands */
/*             pui8Size           -> yields the maximum size of the write memory block (in bytes) (it must be not NULL) */
/* RETURNS: DMACS_OK if success */
/*          DMACS_FAILURE if an error occurred */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: this function may return DMACS_OK also if the detected maximum write size is 0 (write not supported) */
uInt32 DMACSAPI DMacsDetectMaxWriteBlockSize (Int16 i16ChannelNr, uInt8 ui8LDU, uInt8 ui8LSU,
											  uInt16 ui16ReplyTimeout, uInt16 ui16MinSilenceTime,
											  uInt16 ui16MemAddress, uInt8 * pui8Size);


/****************************************************************************/
/*                           DMacsMultipleMemoryRead                        */
/****************************************************************************/
/* TASK: this function performs memory readings minimizing the number of DAAS messages */
/* PARAMETERS: i16ChannelNr       -> the communication channel */
/*             ui8LDU             -> the logical destination unit */
/*             ui8LSU             -> the logical source unit */
/*             ui16ReplyTimeout   -> the reply timeout (in ms) */
/*             ui16MinSilenceTime -> the minimum time interval between consecutive commands (in ms) */
/*             ui8VarNr           -> the number of variables to read */
/*             ui8MaxBlockSize    -> the maximum size in bytes of each data block */
/*             pui16MemAddress    -> the address of each variable to read */
/*             pui8Size           -> the size in bytes of each variable to read */
/*             ppui8Buffers       -> the result buffers (it must be not NULL) */
/*             pui8DataBlocks     -> if success (and not NULL) it yields the actual */
/*                                   number of data blocks (read messages) */
/* RETURNS: DMACS_OK if success */
/*          DMACS_FAILURE if an error occurred */
/*          DMACS_CHANNEL_NOT_AVAILABLE if the specified channel is not available */
/*          DMACS_NOT_SETUP if Direct Macs not yet setup */
/*          DMACS_CHANNEL_CLOSE if the specified channel is closed */
/*          DMACS_INVALID_PARAMETERS if invalid input parameters have been specified */
/* NOTES: none */
uInt32 DMACSAPI DMacsMultipleMemoryRead (Int16 i16ChannelNr, uInt8 ui8LDU, uInt8 ui8LSU,
                                         uInt16 ui16ReplyTimeout, uInt16 ui16MinSilenceTime, 
										 uInt8 ui8VarNr, uInt8 ui8MaxBlockSize,
                                         const uInt16 pui16MemAddress[], const uInt8 pui8Size[],
                                         uInt8 ppui8Buffers[][MAX_VAR_SIZE],
                                         uInt8 * pui8DataBlocks);


#ifdef __cplusplus
        }
#endif

#endif /* DIRECTMACS_H */
