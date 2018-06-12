// MacsView.cpp : main project file.
#include "stdafx.h"

#include <time.h>
#include <conio.h>

#include <Service.h>
#include <Trace.h>
#include <OutBox.h>
#include <Ovc2000.h>
#include <HOC2010.h>

//@@@ver
#define SOFTWARE_VERSION "4.03"

//-----------------------------------------------------------------------------
int main(int argc, char* argv[])
{
  // Message buffer
  struct Message {
    Macs_Header alh;
    uInt8       data[256];
  } message;

  // Button pressed
  int chr;

  // Service
  Service service[10];
  int num_services    = 0;
  int sym_service_idx = -1;
  int key_service_idx = -1;
  int silence_time    = 1000;

  // Configuration
	int Macs_port    = 0;
  char *ini_MacsMsg  = NULL;
  char *ini_MacsView = NULL;

	switch ( argc ) {
    case 4:
      ini_MacsView = argv[3];
    case 3:
      ini_MacsMsg = argv[2];
      sscanf (argv[1], "%d", &Macs_port);
      break;

    default:
      printf("MacsView v.%s                   \n", SOFTWARE_VERSION);
      printf("                                                  \n");
      printf("Usage: MacsView port MacsMsg.ini [MacsView.ini]   \n");
      printf("                                                  \n");
      printf("Options:                                          \n");
      printf(" port          0 = A.M.I.                         \n");
      printf(" MacsMsg.ini   Macs messages configuration file   \n");
      printf(" MacsView.ini  Macs viewer configuration file     \n");
      printf("                                                  \n");
      printf("Keys:                                             \n");
      printf(" Z             exit                               \n");
      printf(" z             select service (if available)      \n");
      printf(" H             reload MacsView.ini (if available) \n");
      printf(" h             service help (if available)        \n");
      return 0;
  }

  // Open Macs
    if(    ( Macs_open( Macs_port, ini_MacsMsg )        )
        || ( Macs_set_address( Macs_address( OBS, 1 ) ) ) ) {
    Macs_close();
    exit(0);
  }

  for( chr = 0; ( chr != 'Z' ); ) {

    // Open ini file
    if ( ini_MacsView != NULL ) {

      int idx;
      dictionary *ini = iniparser_load( ini_MacsView );
      uInt8 address;

      if( ini != NULL) {

        Macs_set_guard_level( iniparser_getint( ini, "MacsView:LogGuardLevel", 0) );
        Macs_set_log_on_stdout( iniparser_getboolean( ini, "MacsView:LogOnStdOut", 0) );
        silence_time = iniparser_getint( ini, "MacsView:SilenceTime", silence_time);
        if( ( address = iniparser_getint( ini, "MacsView:Address", 0 ) ) != 0 ) {
          Macs_set_address( address );
        }

        if( Trace_open( ini, &service[num_services] ) == 0 ) {
          num_services++;
        }
        if( Outbox_open( ini, &service[num_services] ) == 0 ) {
          num_services++;
        }
        if( OVC2000_open( ini, &service[num_services] ) == 0 ) {
          num_services++;
        }
        if( HOC2010_open( ini, &service[num_services] ) == 0 ) {
          num_services++;
        }
        for( idx=0; idx<num_services; idx++ ) {
          if( service[idx].sym != NULL ) {
            sym_service_idx = idx;
          }
          if( service[idx].key_handle != NULL ) {
            key_service_idx = idx;
          }
        }
        if( key_service_idx != -1 ) {
          printf("%% %s:selected\n", service[key_service_idx].name );
        }
      }
      iniparser_freedict( ini );
    }

    {
      uInt8 sym_value[MAX_SYM_SIZE];
      int sym_available   = 0;

      int sym_idx         = 0;
      clock_t time;
      clock_t last_time   = clock();

      for( chr = 0; ( chr !='H' ) && ( chr != 'Z' ); ) {

        // Key events management
        if( kbhit() ) {
          chr = getch();

          if( key_service_idx != -1 ) {

            if ( chr == 'z' ) {
              do {
                if( (++key_service_idx) >= num_services ) {
                  key_service_idx = 0;
                }
              } while( service[key_service_idx].key_handle == NULL);
              printf("%% %s:selected\n", service[key_service_idx].name );
            }
            service[key_service_idx].key_handle( chr );
          }
        }

        { // Service loop management
          int idx;
          for( idx=0; idx<num_services; idx++ ) {
            if( service[idx].loop != NULL ) {
              service[idx].loop( );
            }
          }
        }

        { // Receive messages management
          if( Macs_receive( &message.alh.mlh ) == DMACS_MESSAGE_RECEIVED ) {

            if( sym_service_idx != -1 ) {
              if( Sym_read_rep( service[sym_service_idx].sym[sym_idx], &message.alh, sym_value ) ) {
                sym_available = 1;
              }
            }
            OVC2000_message_handle( &message.alh );
          }
        }

        if( sym_service_idx != -1 ) {

          // Sent messages management
          time = clock();
          if( ( time - last_time ) > silence_time ) {

            last_time = time;

            if ( sym_available == 1 ) {
              sym_available = 0;

              service[sym_service_idx].update( sym_value, sym_idx );

              sym_idx++;
              if( sym_idx >= service[sym_service_idx].num_syms ) {
                sym_idx = 0;
                do {
                  if( (++sym_service_idx) >= num_services ) {
                    sym_service_idx = 0;
                  }
                } while( service[sym_service_idx].sym == NULL);
              }
           }

           Sym_read_req( service[sym_service_idx].sym[sym_idx] );
          }
        }
      }
    }
    for( ; num_services > 0; num_services-- ) {
      service[num_services-1].close();
    }
  }
  Macs_close();
  return 0;
}
