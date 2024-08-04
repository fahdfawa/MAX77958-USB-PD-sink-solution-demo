
////////////MAX32660 code for MAX77958 PD Negotiator////////////////////
//////////////Developed by Fahad Ahammad CAC APR////////////////////////

/***** Includes *****/
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "mxc_device.h"
#include "mxc_delay.h"
#include "nvic_table.h"
#include "gpio.h"
#include "i2c.h"
#include "dma.h"
#include "led.h"
#include "uart.h"
#include "board.h"
#include "Functions.h"


/***** Definitions *****/
//void Register_Read(mxc_i2c_regs_t* i2c_master, uint8_t reg, uint8_t* Read_value);
//void Register_Write(mxc_i2c_regs_t* i2c_master, uint8_t reg, uint8_t Write_value0_LSB);
////void Register_Multi_Read(mxc_i2c_regs_t* i2c_master, uint8_t Read_Addr_strt, uint8_t Read_Addr_end, uint8_t* Read_value, uint8_t* rx_buffer);
//void Register_Multi_Read(mxc_i2c_regs_t* i2c_master, uint8_t start_reg, uint8_t num_regs, uint8_t* Read_values);
// #define MASTERDMA


//#define I2C_SLAVE MXC_I2C1

#define I2C_FREQ 100000
#define I2C_BYTES 100

#define UART_BAUD 115200
#define BUFF_SIZE 255
#define UART0 MXC_UART0
#define UART1 MXC_UART1
#define RXBUF_SIZE 100



/***** Globals *****/


uint8_t tx_buffer[50];
volatile uint8_t DMA_FLAG = 0;
volatile int I2C_FLAG;
volatile int txnum = 0;
volatile int txcnt = 0;
volatile int rxnum = 0;
volatile int num;
uint8_t RxData[BUFF_SIZE];
mxc_uart_regs_t *ConsoleUART = MXC_UART_GET_UART(CONSOLE_UART);
char rxBuf[RXBUF_SIZE];
int Max_byte_len = 4;  //8 datas of 4 bytes is coming
uint8_t receive_buffer1[4];
uint8_t receive_buffer2[4];
uint8_t receive_buffer8[4];
volatile int cnt = 0;
volatile bool crRecv = false;
volatile bool crRecv_quick = false;
int count = 0;
int count_quick =0;
uint32_t PDO[7];
uint32_t PDO_quick[7];
uint8_t Set_sink_PDO_fn_call_flag = 0;
uint8_t Voltage_value, Current_value, PD_Status_value;

void UART1_Handler(void)
{
	MXC_Delay(500000); //Required for the device to response!!


    if (ConsoleUART->int_fl & MXC_F_UART_INT_FL_RX_FIFO_LVL) {
        ConsoleUART->int_fl |= MXC_F_UART_INT_FL_RX_FIFO_LVL;

        while ((ConsoleUART->stat &
                MXC_F_UART_STAT_RX_NUM)) { //Continue to read characters until receive buffer empty

        	     memset(rxBuf, 0x0, RXBUF_SIZE * sizeof(char));

                 rxBuf[0] = (char)MXC_UART_ReadCharacter(ConsoleUART); //Read character



                 if (!strcmp(rxBuf, "T"))
                 {
                	 printf("%c\n",rxBuf[0]);
                 }

                if (!strcmp(rxBuf, "I"))
                {

                	int Max_byte_len = 1;
                	uint8_t receive_buffer[Max_byte_len];
                	MXC_UART_ReadRXFIFO(ConsoleUART, receive_buffer, Max_byte_len);
                	MXC_UART_ClearRXFIFO(ConsoleUART);
					Source_Cap_Req(receive_buffer[0], &src_cap_req_combined);
					memset(rxBuf, 0x0, RXBUF_SIZE * sizeof(char));
                }

                if (!strcmp(rxBuf, "A"))
                {
                	    uint32_t src_PDO1, src_PDO2, src_PDO3, src_PDO4, src_PDO5, src_PDO6, src_PDO7, src_PDO8;
                	    uint8_t Number_of_PDOs;
                	    uint8_t Selected_PDO;
                	    //Calling twice is required due to interrupt clearing
                	    Current_Source_Cap(&curr_src_cap_combined, &Number_of_PDOs, &Selected_PDO, &src_PDO1, &src_PDO2, &src_PDO3, &src_PDO4, &src_PDO5, &src_PDO6, &src_PDO7, &src_PDO8);
                	    MXC_Delay(1000000);
                	    Current_Source_Cap(&curr_src_cap_combined, &Number_of_PDOs, &Selected_PDO, &src_PDO1, &src_PDO2, &src_PDO3, &src_PDO4, &src_PDO5, &src_PDO6, &src_PDO7, &src_PDO8);
                	    //Current_Source_Cap(&curr_src_cap_combined, &Number_of_PDOs, &Selected_PDO, &src_PDO1, &src_PDO2, &src_PDO3, &src_PDO4, &src_PDO5, &src_PDO6, &src_PDO7, &src_PDO8);
                	    printf("%X\n", Number_of_PDOs);
						printf("%X\n", Selected_PDO);
                	    printf("%X\n", src_PDO1);
                		printf("%X\n", src_PDO2);
                		printf("%X\n", src_PDO3);
                		printf("%X\n", src_PDO4);
                		printf("%X\n", src_PDO5);
                		printf("%X\n", src_PDO6);
                		printf("%X\n", src_PDO7);
                		printf("%X\n", src_PDO8);

                		printf("expected_data\n");

                		memset(rxBuf, 0x0, RXBUF_SIZE * sizeof(char));
                }

                if (!strcmp(rxBuf, "B"))
				{
						MXC_UART_ReadRXFIFO(ConsoleUART, receive_buffer1, Max_byte_len);
						crRecv = true;

				}

                if (!strcmp(rxBuf, "C"))
				{
                	uint8_t Num_PDOs;
                	uint32_t snk_PDO1, snk_PDO2, snk_PDO3, snk_PDO4, snk_PDO5, snk_PDO6;

                	Sink_PDO_Req(&snk_PDO_req_combined, &Num_PDOs, &snk_PDO1, &snk_PDO2, &snk_PDO3, &snk_PDO4, &snk_PDO5, &snk_PDO6);
                	MXC_Delay(1000000);
                	Sink_PDO_Req(&snk_PDO_req_combined, &Num_PDOs, &snk_PDO1, &snk_PDO2, &snk_PDO3, &snk_PDO4, &snk_PDO5, &snk_PDO6);
					//Calling twice is required due to interrupt clearing

					printf("%X\n", Num_PDOs);
					printf("%X\n", snk_PDO1);
					printf("%X\n", snk_PDO2);
					printf("%X\n", snk_PDO3);
					printf("%X\n", snk_PDO4);
					printf("%X\n", snk_PDO5);
					printf("%X\n", snk_PDO6);

					printf("expected_data\n");

					memset(rxBuf, 0x0, RXBUF_SIZE * sizeof(char));

				}

                if (!strcmp(rxBuf, "D"))
				{

					Port_Detection_Status_Voltage_current_Read(&Voltage_value, &Current_value, &PD_Status_value);

					printf("expected_data\n");

				}

                if (!strcmp(rxBuf, "E"))
				{

                	uint32_t src_PDO1, src_PDO2, src_PDO3, src_PDO4, src_PDO5, src_PDO6, src_PDO7, src_PDO8;
					uint8_t Number_of_PDOs;
					uint8_t Selected_PDO;
					//Calling twice is required due to interrupt clearing
					Current_Source_Cap(&curr_src_cap_combined, &Number_of_PDOs, &Selected_PDO, &src_PDO1, &src_PDO2, &src_PDO3, &src_PDO4, &src_PDO5, &src_PDO6, &src_PDO7, &src_PDO8);
					MXC_Delay(1000000);
					Current_Source_Cap(&curr_src_cap_combined, &Number_of_PDOs, &Selected_PDO, &src_PDO1, &src_PDO2, &src_PDO3, &src_PDO4, &src_PDO5, &src_PDO6, &src_PDO7, &src_PDO8);
					//Current_Source_Cap(&curr_src_cap_combined, &Number_of_PDOs, &Selected_PDO, &src_PDO1, &src_PDO2, &src_PDO3, &src_PDO4, &src_PDO5, &src_PDO6, &src_PDO7, &src_PDO8);
					printf("%X\n", Number_of_PDOs);
					printf("%X\n", Selected_PDO);
					printf("%X\n", src_PDO1);
					printf("%X\n", src_PDO2);
					printf("%X\n", src_PDO3);
					printf("%X\n", src_PDO4);
					printf("%X\n", src_PDO5);
					printf("%X\n", src_PDO6);
					printf("%X\n", src_PDO7);
					printf("%X\n", src_PDO8);

					printf("expected_data\n");

				}

                if (!strcmp(rxBuf, "F"))
                {

                	int Max_byte_len = 1;
                	uint8_t receive_buffer3[Max_byte_len];
                	MXC_UART_ReadRXFIFO(ConsoleUART, receive_buffer3, Max_byte_len);
                	MXC_UART_ClearRXFIFO(ConsoleUART);
					Source_Cap_Req(receive_buffer3[0], &src_cap_req_combined);
					memset(rxBuf, 0x0, RXBUF_SIZE * sizeof(char));
                }

                if (!strcmp(rxBuf, "G"))
				{
                	int Max_byte_len = 4;
                	uint8_t receive_buffer5[Max_byte_len];
                    MXC_UART_ReadRXFIFO(ConsoleUART, receive_buffer5, Max_byte_len);
                	MXC_UART_ClearRXFIFO(ConsoleUART);
                	uint8_t Term_voltage_rec = receive_buffer5[0];
                	uint8_t Chg_inp_curr_lmt = receive_buffer5[1];
                	uint8_t Fast_chg_curr_lsb = receive_buffer5[2];
                	//uint8_t Fast_chg_curr_msb = receive_buffer5[3];

                	MAX77986_Charger_initial_settings(Term_voltage_rec,Chg_inp_curr_lmt,Fast_chg_curr_lsb);
				}

                if (!strcmp(rxBuf, "H"))
				{
						MXC_UART_ReadRXFIFO(ConsoleUART, receive_buffer8, Max_byte_len);
						crRecv_quick = true;

				}

                if (!strcmp(rxBuf, "J"))
				{
                	int Max_byte_len = 5;
                	uint8_t receive_buffer6[Max_byte_len];
                    MXC_UART_ReadRXFIFO(ConsoleUART, receive_buffer6, Max_byte_len);
                	MXC_UART_ClearRXFIFO(ConsoleUART);
                	uint8_t Enable_PPS = receive_buffer6[0];
                	uint8_t Selected_APDO = receive_buffer6[1];
                	uint8_t Def_Volt_LSB = receive_buffer6[2];
                	uint8_t Def_Volt_MSB = receive_buffer6[3];
                	uint8_t Default_curr = receive_buffer6[4];

                	uint16_t Def_Volt_comb = (0x0FFF & (Def_Volt_MSB << 8 | Def_Volt_LSB))*20;
                	uint16_t Default_curr_scaled = Default_curr * 50;

                	Enable_PPS_Mode(Enable_PPS, 0x00FA, 0x1E);
                	MXC_Delay(500000);   //Delay is important. otherwise won't work
                	Set_PPS_Voltage_Current(Selected_APDO,Def_Volt_comb, Default_curr_scaled);  //default voltage: 5V(0x00FA), default current: 1500mA (0x1E)
				}

                if (!strcmp(rxBuf, "K"))
				{
                	int Max_byte_len = 2;
                	uint8_t receive_buffer7[Max_byte_len];
                    MXC_UART_ReadRXFIFO(ConsoleUART, receive_buffer7, Max_byte_len);
                	MXC_UART_ClearRXFIFO(ConsoleUART);
                	uint8_t BYP_voltage = receive_buffer7[0];
                	uint8_t Rev_curr = receive_buffer7[1];

                	Enable_Reverse_OTG(BYP_voltage,Rev_curr);
				}

            }
        }
}


// *****************************************************************************
int main()
{

    int error = 0;

    //Setup the I2CM
    error = MXC_I2C_Init(I2C_MASTER, 1, 0);

    if (error != E_NO_ERROR) {
        printf("-->Failed master\n");
        return error;
    } else {
        printf("\n-->I2C Master Initialization Complete\n");
    }

    NVIC_EnableIRQ(I2C0_IRQn);

    MXC_I2C_SetFrequency(I2C_MASTER, I2C_FREQ);

    //UART initializations

    memset(RxData, 0x0, BUFF_SIZE);

        NVIC_ClearPendingIRQ(UART1_IRQn);
        NVIC_DisableIRQ(UART1_IRQn);
        MXC_NVIC_SetVector(UART1_IRQn, UART1_Handler);
        NVIC_EnableIRQ(UART1_IRQn);


        if ((error = MXC_UART_Init(UART1, UART_BAUD, MAP_A)) != E_NO_ERROR) {
            printf("-->Error initializing UART: %d\n", error);
            return error;
        }

        printf("-->UART Initialized\n\n");

        mxc_uart_req_t read_req;
    	read_req.uart = UART1;
    	read_req.rxData = RxData;
    	read_req.rxLen = BUFF_SIZE;
    	read_req.txLen = 0;
    	MXC_UART_TransactionAsync(&read_req);

   //GPIO Interrupt Settings

    GPIO_Interrupt_Enable();

    Set_Interrupt_Mask();

    Mask_and_Read_Interrupts();  //setting interrupt mask and clearing all interrupts






//    MXC_Delay(2000000);

  while(1)
  {
	if (crRecv) {
		crRecv = false;
		PDO[count] = 0xFFFFFFFF & (receive_buffer1[3]|receive_buffer1[2]<<8|receive_buffer1[1]<<16|receive_buffer1[0]<<24);
//		uint8_t Comb_Num_PDO_Mem_write = receive_buffer1[4];
		MXC_UART_ClearRXFIFO(ConsoleUART);
		memset(receive_buffer1, 0x0, 4);
		count = count+1;
		if (count == 7){
			count = 0;
			uint8_t MTP_Wrte = ((PDO[6] >> 31) & 0x00000001);
			uint8_t No_of_SNK_PDOs = (PDO[6] >> 24) & 0x00000007;
			MXC_Delay(100000);
			Set_Sink_PDOs(MTP_Wrte, No_of_SNK_PDOs, PDO[0], PDO[1], PDO[2], PDO[3], PDO[4], PDO[5]);
		 }

     }

	if (crRecv_quick) {
		crRecv_quick = false;
		PDO_quick[count_quick] = 0xFFFFFFFF & (receive_buffer8[3]|receive_buffer8[2]<<8|receive_buffer8[1]<<16|receive_buffer8[0]<<24);
//		uint8_t Comb_Num_PDO_Mem_write_quick = receive_buffer8[4];
		MXC_UART_ClearRXFIFO(ConsoleUART);
		memset(receive_buffer8, 0x0, 4);
		count_quick = count_quick+1;
		if (count_quick == 7){
			count_quick = 0;
			uint8_t MTP_Wrte_quick = ((PDO_quick[6] >> 31) & 0x00000001);
			uint8_t No_of_SNK_PDOs_quick = (PDO_quick[6] >> 24) & 0x00000007;
			MXC_Delay(100000);
			Set_Sink_PDOs(MTP_Wrte_quick, No_of_SNK_PDOs_quick, PDO_quick[0], PDO_quick[1], PDO_quick[2], PDO_quick[3], PDO_quick[4], PDO_quick[5]);
		 }

     }


   }


}
















