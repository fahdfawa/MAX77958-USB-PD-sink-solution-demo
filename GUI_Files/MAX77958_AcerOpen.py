import customtkinter as ctk
import serial as sr
import time
import serial.tools.list_ports as list_ports
from tkinter import messagebox
from PIL import Image
import os, sys

s = None
count_ss = 0 
read_back = 0

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")    
    
    return os.path.join(base_path, relative_path)

def show_selected_frame(choice):
    selected_option = choice
    for frame_name, frame in frames.items():
        if frame_name == selected_option:
           frame.place(x=150,y= 60)
    
        else:
            frame.place_forget()

            
def Connect_device():
    global s,connection_event,read_back  # Declare s as a global variable
    selected_COM_port = combobox_com_port.get()
    selected_baud_rate = int(combobox_baud_rate.get())

    try:
        # Open the serial port
        s = sr.Serial(selected_COM_port, selected_baud_rate,timeout = 1)
        s.write(b"T")
        read_back = s.readline().decode("UTF-8").strip()

        if read_back == 'T':
            show_custom_message("Success", "Connection successful")
        else:
            #print("Connection failed")
            show_custom_error_message("Error", "Connection failed")

    except sr.SerialException as e:
        #print(f"Serial port error: {e}")
        show_custom_error_message("Serial Port Error", f"Serial port error: {e}")
    except Exception as e:
       #print(f"An unexpected error occurred: {e}")
        show_custom_error_message("Error", f"An unexpected error occurred: {e}")
        
def Disconnect_device():
    global s
    try:
        if s.is_open:
            s.close()
            #print("Connection closed")
            show_custom_message("Success", "Connection closed")
        else:
            #print("Port is not open")
            show_custom_error_message("Error", "Port is not open")
    except Exception as e:
        #print(f"An unexpected error occurred: {e}")
        show_custom_error_message("Error", f"An unexpected error occurred: {e}")        

def show_custom_message(title, message):
    # Show a custom message dialog with the 'info' icon
    messagebox.showinfo(title, message)

def show_custom_error_message(title, message):
    # Show a custom message dialog with the 'error' icon
    messagebox.showerror(title, message)

    
            
            
def Src_cap_Req():
    PDO_position = Req_PDO_Position_sc_Entry.get()
    PDO_position_split = PDO_position.split("x")
    PDO_position = PDO_position_split[1]
    PDO_position_hex = bytes.fromhex(PDO_position)
    s.write(b"I")
    s.write(PDO_position_hex)
    
def Curr_src_Cap():
    s.write(b"A")
    buffer_sc = []
    while True:
        received_data_sc = s.readline().decode("UTF-8").strip()
        if received_data_sc:
           buffer_sc.append(received_data_sc)
           if received_data_sc == 'expected_data':
              break
          
    buffer_sc.pop()   ## to pop out "expected data from buffer"    
    formatted_buffer_sc = []
    for element in buffer_sc:
        value = int(element, 16)
        formatted_string = f'0x{value:08X}'
        formatted_buffer_sc.append(formatted_string)   
        
    No_of_PDOs_sr_Tb.delete("0.0","end")
    Selected_no_of_PDOs_sr_Tb.delete("0.0","end")
    PDO1_sr_Tb.delete("0.0","end")
    PDO2_sr_Tb.delete("0.0","end")
    PDO3_sr_Tb.delete("0.0","end")
    PDO4_sr_Tb.delete("0.0","end")
    PDO5_sr_Tb.delete("0.0","end")
    PDO6_sr_Tb.delete("0.0","end")
    PDO7_sr_Tb.delete("0.0","end")
    PDO8_sr_Tb.delete("0.0","end")
    
    No_of_PDOs_sr_Tb.insert("0.0","0x" + buffer_sc[0])
    Selected_no_of_PDOs_sr_Tb.insert("0.0","0x" + buffer_sc[1])
    PDO1_sr_Tb.insert("0.0",formatted_buffer_sc[2])
    PDO2_sr_Tb.insert("0.0",formatted_buffer_sc[3])
    PDO3_sr_Tb.insert("0.0",formatted_buffer_sc[4])
    PDO4_sr_Tb.insert("0.0",formatted_buffer_sc[5])
    PDO5_sr_Tb.insert("0.0",formatted_buffer_sc[6])
    PDO6_sr_Tb.insert("0.0",formatted_buffer_sc[7])
    PDO7_sr_Tb.insert("0.0",formatted_buffer_sc[8])
    PDO8_sr_Tb.insert("0.0",formatted_buffer_sc[9])
    
def Set_SNK_PDO():
    
    Memory_write = Read_SNK_PDO_ss_Swh.get()
    No_of_sink_PDOs = int(No_of_PDOs_ss_Etry.get().split("x")[1])
    Comb_mmry_Number = 0xFF & ((Memory_write << 7) | No_of_sink_PDOs)
    
    PDO1 = (PDO1_ss_Etry.get()).split("x")[1]
    PDO2 = (PDO2_ss_Etry.get()).split("x")[1]
    PDO3 = (PDO3_ss_Etry.get()).split("x")[1]
    PDO4 = (PDO4_ss_Etry.get()).split("x")[1]
    PDO5 = (PDO5_ss_Etry.get()).split("x")[1]
    PDO6 = (PDO6_ss_Etry.get()).split("x")[1]
    
    Comb_mmry_Number_bytes = Comb_mmry_Number.to_bytes(1, byteorder='big')
    PDO1_hex = bytes.fromhex(PDO1)
    PDO2_hex = bytes.fromhex(PDO2)
    PDO3_hex = bytes.fromhex(PDO3)
    PDO4_hex = bytes.fromhex(PDO4)
    PDO5_hex = bytes.fromhex(PDO5)
    PDO6_hex = bytes.fromhex(PDO6)
    
   # print(Concatenated_PDOs_hex)
    # Write the bytes to the serial port
    sleeptime = 0.5
    time.sleep(sleeptime)
    
    s.write(b'B')
    s.write(PDO1_hex)
    time.sleep(sleeptime)
    
    s.write(b'B')
    s.write(PDO2_hex)
    time.sleep(sleeptime)
    
    s.write(b'B')
    s.write(PDO3_hex)
    time.sleep(sleeptime)
    
    s.write(b'B')
    s.write(PDO4_hex)
    time.sleep(sleeptime)
    
    s.write(b'B')
    s.write(PDO5_hex)
    time.sleep(sleeptime)
    
    s.write(b'B')
    s.write(PDO6_hex)
    time.sleep(sleeptime)
    
    s.write(b'B')
    s.write(Comb_mmry_Number_bytes)   
    
def SNK_PDO_REQ():
    s.write(b'C')
    buffer_sp = []
    while True:
        received_data_sp = s.readline().decode("UTF-8").strip()
        if received_data_sp:
           buffer_sp.append(received_data_sp)
           if received_data_sp == 'expected_data':
              break
    
    buffer_sp.pop()     
    formatted_buffer_sp = []
    for element in buffer_sp:
        value_sp = int(element, 16)
        formatted_string_sp = f'0x{value_sp:08X}'
        formatted_buffer_sp.append(formatted_string_sp)      
          
    No_of_PDOs_sp_Tb.delete("0.0","end")
    PDO1_sp_Tb.delete("0.0","end")
    PDO2_sp_Tb.delete("0.0","end")
    PDO3_sp_Tb.delete("0.0","end")
    PDO4_sp_Tb.delete("0.0","end")
    PDO5_sp_Tb.delete("0.0","end")
    PDO6_sp_Tb.delete("0.0","end")
    
    No_of_PDOs_sp_Tb.insert("0.0","0x" + buffer_sp[0])
    PDO1_sp_Tb.insert("0.0",formatted_buffer_sp[1])
    PDO2_sp_Tb.insert("0.0",formatted_buffer_sp[2])
    PDO3_sp_Tb.insert("0.0",formatted_buffer_sp[3])
    PDO4_sp_Tb.insert("0.0",formatted_buffer_sp[4])
    PDO5_sp_Tb.insert("0.0",formatted_buffer_sp[5])
    PDO6_sp_Tb.insert("0.0",formatted_buffer_sp[6])
    
def Check_Status():
    s.write(b'D')
    buffer_stat = []
    
    while True:
        received_data_stat = s.readline().decode("UTF-8").strip()
        if received_data_stat:
           buffer_stat.append(received_data_stat)
           if received_data_stat == 'expected_data':
              break
    
    buffer_stat.pop()
    
    Charger_Detec_Tb.delete("0.0","end")
    VBUS_ADC_Tb.delete("0.0","end")
    CC_Pin_det_max_ct_Tb.delete("0.0","end")
    VBUS_Detec_Tb.delete("0.0","end")
    CC_Pin_state_mac_det_Tb.delete("0.0","end")
    Active_cc_pin_Tb.delete("0.0","end")
    VSAFE0V_status_Tb.delete("0.0","end")
    PD_Message_Tb.delete("0.0","end")
    PSRDY_Status_Tb.delete("0.0","end")
    Power_Role_Tb.delete("0.0","end")
    Data_Role_Tb.delete("0.0","end")
    
    Charger_Detec_Tb.insert("0.0",buffer_stat[0])
    VBUS_ADC_Tb.insert("0.0",buffer_stat[1])
    CC_Pin_det_max_ct_Tb.insert("0.0",buffer_stat[2])
    VBUS_Detec_Tb.insert("0.0",buffer_stat[3])
    CC_Pin_state_mac_det_Tb.insert("0.0",buffer_stat[4])
    Active_cc_pin_Tb.insert("0.0",buffer_stat[5])
    VSAFE0V_status_Tb.insert("0.0",buffer_stat[6])
    PD_Message_Tb.insert("0.0",buffer_stat[7])
    PSRDY_Status_Tb.insert("0.0",buffer_stat[8])
    Power_Role_Tb.insert("0.0",buffer_stat[9])
    Data_Role_Tb.insert("0.0",buffer_stat[10])    
    
def Read_Quick_PDO_Voltage():
    s.write(b'E')
    
    
    buffer_quick_sc = []
    while True:
        received_data_quick_sc = s.readline().decode("UTF-8").strip()
        if received_data_quick_sc:
           buffer_quick_sc.append(received_data_quick_sc)
           if received_data_quick_sc == 'expected_data':
              break
          
    buffer_quick_sc.pop()    
    formatted_buffer_quick_sc = []
    for element in buffer_quick_sc:
        value = int(element, 16)
        formatted_string_quick = f'0x{value:08X}'
        formatted_buffer_quick_sc.append(formatted_string_quick)   
        
    formatted_buffer_quick_PDOS_sc = formatted_buffer_quick_sc[2:]
    text_added_buff_quick_PDOs_sc = []
    
    for index, item in enumerate(formatted_buffer_quick_PDOS_sc,start = 1):
        item_hex  =int(item,16)
        if (item_hex >> 28 & 0b1111) == 0b0000:
            decimal_value_current = (item_hex & 0x000003FF)*10
            decimal_value_voltage = ((item_hex & 0x000FFC00) >> 10)*50     
            text_to_add = f'PDO{index}: {decimal_value_voltage}mV/{decimal_value_current}mA'

        elif (item_hex >> 28 & 0b1111) == 0b1100:
             decimal_value_curr_pps = (item_hex & 0x000000FF)*50
             decimal_value_pps_min_voltage = ((item_hex >> 8) & 0xFF)*100
             decimal_value_pps_max_voltage = ((item_hex >> 18) & 0xFF)*200
             text_to_add = f'PDO{index}:  {decimal_value_pps_min_voltage}mV - {decimal_value_pps_max_voltage}mV/{decimal_value_curr_pps}mA'
        
        else: 
             text_to_add = f'PDO{index}: Not available'
        text_added_buff_quick_PDOs_sc.append(text_to_add)    
        
    No_of_PDOs_quick_run_Tb.delete("0.0","end")
    Curr_PDO_Pos_quick_Tb.delete("0.0","end")
    
    No_of_PDOs_quick_run_Tb.insert("0.0",buffer_quick_sc[0])
    Curr_PDO_Pos_quick_Tb.insert("0.0",buffer_quick_sc[1])  
    
    Set_PDO_quick_combo.set("Set PDO")  # set initial value
    Set_PDO_quick_combo.configure(values=text_added_buff_quick_PDOs_sc)
    
def Set_Quick_PDO_Voltage():
    
    selected_PDO_quick = Set_PDO_quick_combo.get()
    selected_PDO_quick = selected_PDO_quick[:4]
        
    if selected_PDO_quick == 'PDO1':
       position_quick =   '01'
    elif selected_PDO_quick == 'PDO2':
         position_quick = '02'   
    elif selected_PDO_quick == 'PDO3':
         position_quick = '03'     
    elif selected_PDO_quick == 'PDO4':
         position_quick = '04'      
    elif selected_PDO_quick == 'PDO5':
         position_quick = '05'  
    elif selected_PDO_quick == 'PDO6':
         position_quick = '06'  
    elif selected_PDO_quick == 'PDO7':
         position_quick = '07'         
    elif selected_PDO_quick == 'PDO8':
         position_quick = '08'

    position_quick_hex = bytes.fromhex(position_quick)
    
    s.write(b'F')
    s.write(position_quick_hex)
    
def hex_to_chg_term_voltage(hex_value_chg_term):
    
    min_voltage = 4.1500
    step_width = 0.0125
    # Calculate the voltage using linear mapping
    voltage = min_voltage + (int(hex_value_chg_term,16) * step_width)
    formatted_voltage = f"{voltage:.3f}"
    return formatted_voltage    
    
       
def Charge_Termiantn_Volt_Set(voltage):
    volt = int(Chg_term_vg_slider.get())
    volt_hex= hex(volt).upper()
    volt_dec = hex_to_chg_term_voltage(volt_hex)
    Chg_term_vg_Tb.delete("0.0","end")
    text_chg_term = f"{volt_hex}  =  {volt_dec}"
    Chg_term_vg_Tb.insert("0.0",text_chg_term)


def hex_to_chgin_limit(hex_value_curr_inp_limit):
    
    min_chg_ct = 0
    step_width_ct = 0.050

    
    # Calculate the voltage using linear mapping
    min_chg_ct_limit = min_chg_ct + (int(hex_value_curr_inp_limit,16) - 3) * step_width_ct
    formatted_chg_ct_lim = f"{min_chg_ct_limit:.3f}"
    return formatted_chg_ct_lim    
    
       
def Charge_Termiantn_chg_lct_lim_Set(voltage):
    
    chg_limit_ct = int(Charger_input_current_slider.get())
    chgin_limit_ct_hex= hex(chg_limit_ct).upper()
    chgin_ct_dec = hex_to_chgin_limit(chgin_limit_ct_hex)
    Charger_input_current_Tb.delete("0.0","end")
    text_cur_ct_term = f"{chgin_limit_ct_hex}  =  {chgin_ct_dec}"
    Charger_input_current_Tb.insert("0.0",text_cur_ct_term)    
    
    
def hex_Fast_chg_limit(hex_value_fast_chg_limit):
    
    min_fast_ct = 0.050
    step_width_fast_ct = 0.0500

    
    # Calculate the voltage using linear mapping
    min_fast_ct_limit = min_fast_ct + int(hex_value_fast_chg_limit,16)* step_width_fast_ct
    formatted_fast_ct_lim = f"{min_fast_ct_limit:.5f}"
    return formatted_fast_ct_lim    
    
       
def Charge_Termiantn_fast_lim_Set(fast_current):
    
    fast_ct = int(Fast_Charge_slider.get())
    fast_ct_hex= hex(fast_ct).upper()
    fast_ct_dec = hex_Fast_chg_limit(fast_ct_hex)
    Fast_Charge_Tb.delete("0.0","end")
    text_cur_ct_term = f"{fast_ct_hex}  =  {fast_ct_dec}"
    Fast_Charge_Tb.insert("0.0",text_cur_ct_term)      


def Initialize_Charger():
    
    try:
        term_vg_dec = int(Chg_term_vg_slider.get())
        Charger_inp_dec = int(Charger_input_current_slider.get())
        Fast_curr_dec = int(Fast_Charge_slider.get())
        
        # Check if the decimal values are within a valid range (0-255 for one byte)
        if 0 <= term_vg_dec <= 31 and 0 <= Charger_inp_dec <= 109 and 0 <= Fast_curr_dec <= 110:
            hex_string_term_vg = f"{term_vg_dec:02X}"
            term_reg_value = bytes.fromhex(hex_string_term_vg)
            
            hex_string_curr_inp = f"{Charger_inp_dec:02X}"
            curr_inp_reg_value = bytes.fromhex(hex_string_curr_inp)
            
            high_byte = (Fast_curr_dec >> 8) & 0xFF  # Shift 8 bits to the right to get the high byte
            low_byte = Fast_curr_dec & 0xFF  # Get the low byte

            # Convert the high and low bytes to bytes objects
            high_byte_bytes_Ft_ct = bytes([high_byte])  ###USED FOR MAX77962 Charger
            low_byte_bytes_Ft_ct = bytes([low_byte])
            
            s.write(b'G')
            s.write(term_reg_value)
            s.write(curr_inp_reg_value)
            s.write(low_byte_bytes_Ft_ct)
            #s.write(high_byte_bytes_Ft_ct)  ###Disabled for MAX77986 single cell charger
        else:
            print("Invalid decimal values. Ensure they are in the range 0-255.")
    except ValueError as e:
        print(f"ValueError: {e}")
        
    
def Sent_quick_Sink_PDO_helper(No_of_Sink_PDOs_quick, Memory_write_quick, SNK_PDO1, SNK_PDO2, SNK_PDO3, SNK_PDO4, SNK_PDO5, SNK_PDO6):
    
    Comb_mmry_Number_quick = 0xFF & ((Memory_write_quick << 7) | No_of_Sink_PDOs_quick)
    Comb_mmry_Number_bytes_quick = Comb_mmry_Number_quick.to_bytes(1, byteorder='big')

    
    sleeptime_quick = 0.5
    time.sleep(sleeptime_quick)
    
    s.write(b'H')
    s.write(SNK_PDO1)
    time.sleep(sleeptime_quick)
    
    s.write(b'H')
    s.write(SNK_PDO2)
    time.sleep(sleeptime_quick)
    
    s.write(b'H')
    s.write(SNK_PDO3)
    time.sleep(sleeptime_quick)
    
    s.write(b'H')
    s.write(SNK_PDO4)
    time.sleep(sleeptime_quick)
    
    s.write(b'H')
    s.write(SNK_PDO5)
    time.sleep(sleeptime_quick)
    
    s.write(b'H')
    s.write(SNK_PDO6)
    time.sleep(sleeptime_quick)  
    
    s.write(b'H')
    s.write(Comb_mmry_Number_bytes_quick)
   
    
    
    
def Set_Plugin_Initial_Voltage(): 
    buffer_quick_Sink_PDOs = ['1401912C', '0002D12C', '0004B12C','00000000','00000000','00000000']
    Sink_quick_PDO0 = bytes.fromhex(buffer_quick_Sink_PDOs[5])
    Sink_quick_PDO1 = bytes.fromhex(buffer_quick_Sink_PDOs[0])
    Sink_quick_PDO2 = bytes.fromhex(buffer_quick_Sink_PDOs[1])
    Sink_quick_PDO3 = bytes.fromhex(buffer_quick_Sink_PDOs[2])
    Sink_quick_PDO4 = bytes.fromhex(buffer_quick_Sink_PDOs[3])
    #Sink_quick_PDO5 = bytes.fromhex(buffer_quick_Sink_PDOs[4])   //Required for future purpose
    #Sink_quick_PDO6 = bytes.fromhex(buffer_quick_Sink_PDOs[5])   //Required for future purpose 
 

    if Initial_Voltage_Combo.get() == '5V/3A':
         Sent_quick_Sink_PDO_helper(1, 1, Sink_quick_PDO1, Sink_quick_PDO0,Sink_quick_PDO0,Sink_quick_PDO0,Sink_quick_PDO0,Sink_quick_PDO0)
    elif Initial_Voltage_Combo.get() == '9V/3A':
         Sent_quick_Sink_PDO_helper(2, 1, Sink_quick_PDO1, Sink_quick_PDO2,Sink_quick_PDO0,Sink_quick_PDO0,Sink_quick_PDO0,Sink_quick_PDO0)
    elif Initial_Voltage_Combo.get() == '15V/3A':
         Sent_quick_Sink_PDO_helper(3, 1, Sink_quick_PDO1, Sink_quick_PDO2,Sink_quick_PDO3,Sink_quick_PDO0,Sink_quick_PDO0,Sink_quick_PDO0)         
    elif Initial_Voltage_Combo.get() == '20V/3A':
         Sent_quick_Sink_PDO_helper(4, 1, Sink_quick_PDO1, Sink_quick_PDO2,Sink_quick_PDO3,Sink_quick_PDO4,Sink_quick_PDO0,Sink_quick_PDO0)            

    

def hex_PPS_Volt_limit(hex_value_PPS_Volt_limit):   
    min_PPS_volt = 0.000
    step_width_PPS_volt = 0.020
    # Calculate the voltage using linear mapping
    PPS_voltage_value = min_PPS_volt + int(hex_value_PPS_Volt_limit,16)* step_width_PPS_volt
    formatted_PPS_Volt_lim = f"{PPS_voltage_value:.3f}"
    return formatted_PPS_Volt_lim 

def hex_PPS_Curr_limit(hex_value_PPS_Curr_limit):   
    min_PPS_curr = 0.000
    step_width_PPS_curr = 0.050
    # Calculate the voltage using linear mapping
    PPS_current_value = min_PPS_curr + int(hex_value_PPS_Curr_limit,16)* step_width_PPS_curr
    formatted_PPS_Curr_lim = f"{PPS_current_value:.3f}"
    return formatted_PPS_Curr_lim

def Display_PPS_Voltage(volt):
    PPS_Voltage_dis = int(PPS_Volt_slider.get())
    PPS_Voltage_dis_hex = hex(PPS_Voltage_dis).upper()
    PPS_Voltage_dis_dec = hex_PPS_Volt_limit(PPS_Voltage_dis_hex)
    PPS_volt_Tb.delete("0.0","end")
    text_PPS_volt_Tb = f"{PPS_Voltage_dis_dec}"
    PPS_volt_Tb.insert("0.0",text_PPS_volt_Tb)
    
def Display_PPS_Current(curr):
    PPS_Current_dis = int(PPS_curr_slider.get())
    PPS_Current_dis_hex = hex(PPS_Current_dis).upper()
    PPS_Current_dis_dec = hex_PPS_Curr_limit(PPS_Current_dis_hex)
    PPS_curr_Tb.delete("0.0","end")
    text_PPS_curr_Tb = f"{PPS_Current_dis_dec}"
    PPS_curr_Tb.insert("0.0",text_PPS_curr_Tb)    
    
      

def Set_PPS_Mode_Volt_Curr():
    PPS_Enable = bytes([PPS_Enable_togg_sw.get()])
    PDO_Selected = bytes([int(Select_APDO_Combo.get()[9])])
    
    try:
        PPS_volt_dec = int(PPS_Volt_slider.get())
        PPS_curr_dec = int(PPS_curr_slider.get())
        
        # Check if the decimal values are within a valid range (0-255 for one byte)
        if 0 <= PPS_volt_dec <= 1000 and 0 <= PPS_curr_dec <= 124:
            
            hex_string_PPS_curr = f"{PPS_curr_dec:02X}"
            PPS_curr_reg_value = bytes.fromhex(hex_string_PPS_curr)
            
            high_byte = (PPS_volt_dec >> 8) & 0xFF  # Shift 8 bits to the right to get the high byte
            low_byte = PPS_volt_dec & 0xFF  # Get the low byte
    
            # Convert the high and low bytes to bytes objects
            high_byte_bytes_PPS_volt = bytes([high_byte])
            low_byte_bytes_PPS_volt = bytes([low_byte])
            
            s.write(b'J')
            s.write(PPS_Enable)
            s.write(PDO_Selected)
            s.write(low_byte_bytes_PPS_volt)
            s.write(high_byte_bytes_PPS_volt)
            s.write(PPS_curr_reg_value)
            
            print(PPS_Enable)
            print(PDO_Selected)
            print(low_byte_bytes_PPS_volt)
            print(high_byte_bytes_PPS_volt)
            print(PPS_curr_reg_value)

        else:
            print("Invalid decimal values. Ensure they are in the range 0-255.")
    except ValueError as e:
        print(f"ValueError: {e}")  
        
        




def hex_OTG_Volt_limit(hex_value_OTG_Volt_limit): 
    min_OTG_volt = 5.0
    step_width_OTG_volt = 0.1
    # Calculate the voltage using linear mapping
    OTG_voltage_value = min_OTG_volt + int(hex_value_OTG_Volt_limit,16)* step_width_OTG_volt
    formatted_OTG_Volt_lim = f"{OTG_voltage_value:.1f}"
    return formatted_OTG_Volt_lim        

def hex_OTG_Curr_limit(hex_value_OTG_Curr_limit):
    min_OTG_curr = 0.5
    step_width_OTG_curr = 0.1
    # Calculate the voltage using linear mapping
    OTG_current_value = min_OTG_curr + int(hex_value_OTG_Curr_limit,16)* step_width_OTG_curr
    formatted_OTG_Curr_lim = f"{OTG_current_value:.3f}"
    return formatted_OTG_Curr_lim    
              
def Display_OTG_Voltage(volts):
    OTG_Voltage_dis = int(Reverse_voltage_slider.get())
    OTG_Voltage_dis_hex = hex(OTG_Voltage_dis).upper()
    OTG_Voltage_dis_dec = hex_OTG_Volt_limit(OTG_Voltage_dis_hex)
    Reverse_voltage_Tb.delete("0.0","end")
    text_OTG_volt_Tb = f"{OTG_Voltage_dis_hex}  =  {OTG_Voltage_dis_dec}"
    Reverse_voltage_Tb.insert("0.0",text_OTG_volt_Tb)

def Display_OTG_Current(currs):
    OTG_Current_dis = int(Reverse_current_limit_slider.get())
    OTG_Current_dis_hex = hex(OTG_Current_dis).upper()
    OTG_Current_dis_dec = hex_OTG_Curr_limit(OTG_Current_dis_hex)
    Rev_curr_limit_Tb.delete("0.0","end")
    text_OTG_curr_Tb = f"{OTG_Current_dis_hex}  =  {OTG_Current_dis_dec}"
    Rev_curr_limit_Tb.insert("0.0",text_OTG_curr_Tb)                    
        
def Reverse_OTG_Mode():
    try:
        Reverse_voltage_dec = int(Reverse_voltage_slider.get())
        Rev_curr_lim_dec = int(Reverse_current_limit_slider.get())
        
        # Check if the decimal values are within a valid range (0-255 for one byte)
        if 0 <= Reverse_voltage_dec <= 70 and 0 <= Rev_curr_lim_dec <= 26:
            
            hex_string_rev_volt = f"{Reverse_voltage_dec:02X}"
            rev_volt_reg_value = bytes.fromhex(hex_string_rev_volt)
            
            hex_string_rev_curr_lim = f"{Rev_curr_lim_dec:02X}"
            rev_curr_lim_reg_value = bytes.fromhex(hex_string_rev_curr_lim)
            
            
            s.write(b'K')
            s.write(rev_volt_reg_value)
            s.write(rev_curr_lim_reg_value)

        else:
            print("Invalid decimal values. Ensure they are in the range 0-255.")
    except ValueError as e:
        print(f"ValueError: {e}")
    
        
        
root = ctk.CTk()
root.title("MAX77958 GUI")
##p1 = ImageTk.PhotoImage(file = 'ADI_Trinamics.png')
# icon_path = resource_path('ADI_Trinamics.ico')

# # Now, you can set the icon for your tkinter root window
# root.iconbitmap(icon_path)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

tabControl = ctk.CTkTabview(root)
tabControl.pack(expand = 1, fill ="both")

tab0 = tabControl.add("Setup")
tab1 = tabControl.add("Status")
tab2 = tabControl.add("Commands")
tab3 = tabControl.add("Quick Run")
tab4 = tabControl.add("OTG Settings")


frames = {}

"""tab0"""

frame50 = ctk.CTkFrame(tab0, width=700, height=200, border_width=3)
frame50.grid(row=0, column=0, padx=50, pady=50,sticky = 'n')
frame50.grid_propagate(False)

frame90 = ctk.CTkFrame(tab0, width=700, height=400, border_width=3)
frame90.grid(row=0, column=0, padx=50, pady=300,sticky = 'n')
frame90.grid_propagate(False)

frame91 = ctk.CTkFrame(tab0, width=640, height=650, border_width=3)
frame91.grid(row=0, column=1, padx=10, pady=50,sticky = 'n')
frame91.grid_propagate(False)


Serial_Port_label = ctk.CTkLabel(frame50, text="Select COM port", width=20,font=("Helvetica", 16))
Serial_Port_label.grid(row=0, column=0, padx=100, pady=20)

Serial_Baud_label = ctk.CTkLabel(frame50, text="Select Baud Rate", width=20,font=("Helvetica", 16))
Serial_Baud_label.grid(row=1, column=0, padx=10, pady=10)

available_ports = [port.device for port in list_ports.comports()]

combobox_com_port = ctk.CTkComboBox(frame50, values=available_ports, text_color="White", width = 250)

combobox_com_port.grid(row=0, column=1, padx=10, pady=10)

options_baud_rates = ["9600","19200","57600","115200","576000","1152000"]
combobox_baud_rate = ctk.CTkComboBox(frame50, values=options_baud_rates, text_color="White", width = 250)

combobox_baud_rate.grid(row=1, column=1, padx=10, pady=10)

Connect_Btn = ctk.CTkButton(frame50,width = 100, height =20, text = "Connect",command = Connect_device,border_width = 2)
Connect_Btn.grid(row = 2, column = 1, padx = 10, pady= 20,sticky = 'w')

DisConnect_Btn = ctk.CTkButton(frame50,width = 100, height =20, text = "Disconnect",command = Disconnect_device,border_width = 2)
DisConnect_Btn.grid(row = 2, column = 1, padx = 10, pady= 20,sticky = 'e')




MAX77958_Image = ctk.CTkImage(dark_image= Image.open(resource_path("MAX77986_DIAGRAM.png")),size=(630,530))
MAX77958_Image_Label = ctk.CTkLabel(tab0, image =MAX77958_Image,text = '')
MAX77958_Image_Label.grid(row=0,column=1,padx =25,pady =110,sticky="NW")




Block_dia_Image = ctk.CTkImage(dark_image= Image.open(resource_path("BlockDiagram1.png")),size=(600,260))
Block_dia_Image_Label = ctk.CTkLabel(frame90, image =Block_dia_Image,text = '')
Block_dia_Image_Label.grid(row=0,column=0,padx =25,pady = 65,sticky="n")




# =============================================================================
# frame51 = ctk.CTkFrame(tab0, width=200, height=50, border_width=3)
# frame51.grid(row=0, column=1, padx=100, pady=400,sticky = "W")
# frame51.grid_propagate(False)
# =============================================================================



# =============================================================================
# 
# options_baud_rates = ["9600","19200","57600","115200","576000","1152000"]
# combobox_baud_rates = ctk.CTkComboBox(tab2, values=options_baud_rates,command=show_baud_rates, text_color="White", width = 250)
# combobox_baud_rates.set("select")  # set initial value
# combobox_baud_rates.grid(row=1, column=1, padx=10, pady=10, sticky="w")
# =============================================================================
"""tab1"""
frame60 = ctk.CTkFrame(tab1, width=1225, height=670, border_width=3)
frame60.grid(row=0, column=0, padx=150, pady=50, sticky = "NE")
frame60.grid_propagate(False)


frame61 = ctk.CTkFrame(frame60, width=500, height=180, border_width=3)
frame61.grid(row=0, column=0, padx=20, pady=20, sticky = "NW")
frame61.grid_propagate(False)

frame62 = ctk.CTkFrame(frame60, width=660, height=180, border_width=3)
frame62.grid(row=0, column=1, padx=0, pady=20, sticky = "NW")
frame62.grid_propagate(False)

frame63 = ctk.CTkFrame(frame60, width=500, height=280, border_width=3)
frame63.grid(row=1, column=0, padx=20, sticky = "NW")
frame63.grid_propagate(False)

frame64 = ctk.CTkFrame(frame60, width=660, height=280, border_width=3)
frame64.grid(row=1, column=1, padx=0, sticky = "NW")
frame64.grid_propagate(False)

frame65 = ctk.CTkFrame(frame60, width=500, height=130, border_width=3)
frame65.grid(row=2, column=0, padx=20,pady =20, sticky = "NW")
frame65.grid_propagate(False)

frame66 = ctk.CTkFrame(frame60, width=660, height=130, border_width=3)
frame66.grid(row=2, column=1, padx=0,pady =20, sticky = "NW")
frame66.grid_propagate(False)


###########Device Details#####################
Device_Details_Lab = ctk.CTkLabel(frame61, text="Device Details", width = 10,font=("Helvetica", 14))
Device_Details_Lab.grid(row = 0, column = 0, padx = 7 , pady = 8,sticky = "w")

Device_ID_Lab = ctk.CTkLabel(frame61, text="Device ID", width = 8,font=("Helvetica", 14))
Device_ID_Lab.grid(row = 1, column = 0, padx = 7 , pady = 1,sticky = "w")

Device_Rev_Lab = ctk.CTkLabel(frame61, text="Device Rev", width = 8,font=("Helvetica", 14))
Device_Rev_Lab.grid(row = 2, column = 0, padx = 7 , pady = 1,sticky = "w")

Firmware_Rev_Lab = ctk.CTkLabel(frame61, text="Firmware Rev", width = 8,font=("Helvetica", 14))
Firmware_Rev_Lab.grid(row = 3, column = 0, padx = 7 , pady = 1,sticky = "w")

Firmware_sub_ver_Lab = ctk.CTkLabel(frame61, text="Frimware Sub ver", width = 8,font=("Helvetica", 14))
Firmware_sub_ver_Lab.grid(row = 4, column = 0, padx = 7 , pady = 1,sticky = "w")

Device_ID_Tb = ctk.CTkTextbox(frame61,width = 150, height =0)
Device_ID_Tb.grid(row = 1, column = 1, padx = 10, pady= 0)

Device_Rev_Tb = ctk.CTkTextbox(frame61,width = 150, height =0)
Device_Rev_Tb.grid(row = 2, column = 1, padx = 10, pady= 0)

Firm_Rev_Tb = ctk.CTkTextbox(frame61,width = 150, height =0)
Firm_Rev_Tb.grid(row = 3, column = 1, padx = 10, pady= 0)

Firm_sub_ver_Tb = ctk.CTkTextbox(frame61,width = 150, height =0)
Firm_sub_ver_Tb.grid(row = 4, column = 1, padx = 10, pady= 0)

Inv_lab4 = ctk.CTkLabel(frame61, text="", width = 100)
Inv_lab4.grid(row = 0, column = 1, padx = 7 , pady = 8,sticky = "w")

Device_Details_write = ctk.CTkButton(frame61,width = 80, height =10, text = "Write")
Device_Details_write.grid(row = 0, column = 2, padx = 10, pady= 1,sticky = "w")

Device_Details_read = ctk.CTkButton(frame61,width = 80, height =10, text = "Read")
Device_Details_read.grid(row = 0, column = 3, padx = 10, pady= 1,sticky = "w")



#########PD Interrupts##########
PD_Interrupts_Lab = ctk.CTkLabel(frame62, text="PD Interrupts", width = 10,font=("Helvetica", 14))
PD_Interrupts_Lab.grid(row = 0, column = 0, padx = 7 , pady = 8,sticky = "w")

Disp_port_Intrrpt_Lab = ctk.CTkLabel(frame62, text="Display Port Interrupt", width = 8,font=("Helvetica", 14))
Disp_port_Intrrpt_Lab.grid(row = 1, column = 0, padx = 7 , pady = 2,sticky = "w")

Data_Role_Intrrpt_Lab = ctk.CTkLabel(frame62, text="Data Role Change Interrupt", width = 8,font=("Helvetica", 14))
Data_Role_Intrrpt_Lab.grid(row = 2, column = 0, padx = 7 , pady = 2,sticky = "w")

PSRDY_Intrrpt_Lab = ctk.CTkLabel(frame62, text="PSRDY Message Interrupt", width = 8,font=("Helvetica", 14))
PSRDY_Intrrpt_Lab.grid(row = 3, column = 0, padx = 7 , pady = 2,sticky = "w")

PS_Message_Intrrpt_Lab = ctk.CTkLabel(frame62, text="PS Message Interrupt", width = 8,font=("Helvetica", 14))
PS_Message_Intrrpt_Lab.grid(row = 4, column = 0, padx = 7 , pady = 2,sticky = "w")

Inv_lab3 = ctk.CTkLabel(frame62, text="", width = 100)
Inv_lab3.grid(row = 0, column = 1, padx = 40 , pady = 8,sticky = "w")

CC_Intrrpt_Btn_write = ctk.CTkButton(frame62,width = 80, height =10, text = "Write")
CC_Intrrpt_Btn_write.grid(row = 0, column = 2, padx = 10, pady= 1,sticky = "w")

PD_Intrrpt_Btn_read = ctk.CTkButton(frame62,width = 80, height =10, text = "Read")
PD_Intrrpt_Btn_read.grid(row = 0, column = 3, padx = 10, pady= 1,sticky = "w")

Disp_port_Intrrt_togg_sw = ctk.CTkSwitch(frame62,width = 220, text="")
Disp_port_Intrrt_togg_sw.grid(row = 1, column = 1, padx = 20 , pady = 2, sticky = "w")

Data_Role_Intrrt_togg_sw = ctk.CTkSwitch(frame62,width = 220, text="")
Data_Role_Intrrt_togg_sw.grid(row = 2, column = 1, padx = 20 , pady = 2, sticky = "w")

PSRDY_Intrrt_togg_sw = ctk.CTkSwitch(frame62,width = 220, text="")
PSRDY_Intrrt_togg_sw.grid(row = 3, column = 1, padx = 20 , pady = 2, sticky = "w")

PS_Message_Intrrt_togg_sw = ctk.CTkSwitch(frame62,width = 220, text="")
PS_Message_Intrrt_togg_sw.grid(row = 4, column = 1, padx = 20 , pady = 2, sticky = "w")


#########CC Interrupts###########

CC_Interrupts_Lab = ctk.CTkLabel(frame63, text="CC Interrupts", width = 10,font=("Helvetica", 14))
CC_Interrupts_Lab.grid(row = 0, column = 0, padx = 7 , pady = 8,sticky = "w")

CC_Stat_Intrrpt_Lab = ctk.CTkLabel(frame63, text="CC STAT Interrupt", width = 8,font=("Helvetica", 14))
CC_Stat_Intrrpt_Lab.grid(row = 1, column = 0, padx = 7 , pady = 0,sticky = "w")

CCVCN_Stat_Intrrpt_Lab = ctk.CTkLabel(frame63, text="CCVCNSTAT Interrupt", width = 8,font=("Helvetica", 14))
CCVCN_Stat_Intrrpt_Lab.grid(row = 2, column = 0, padx = 7 , pady = 0,sticky = "w")

CCI_Stat_Intrrpt_Lab = ctk.CTkLabel(frame63, text="CCISTAT Interrupt", width = 8,font=("Helvetica", 14))
CCI_Stat_Intrrpt_Lab.grid(row = 3, column = 0, padx = 7 , pady = 0,sticky = "w")

CCPIN_Stat_Intrrpt_Lab = ctk.CTkLabel(frame63, text="CCPINSTAT Interrupt", width = 8,font=("Helvetica", 14))
CCPIN_Stat_Intrrpt_Lab.grid(row = 4, column = 0, padx = 7 , pady = 0,sticky = "w")

Moisture_Intrrpt_Lab = ctk.CTkLabel(frame63, text="Moisture Interrupt", width = 8,font=("Helvetica", 14))
Moisture_Intrrpt_Lab.grid(row = 5, column = 0, padx = 7 , pady = 0,sticky = "w")

CC_det_abrt_Intrrpt_Lab = ctk.CTkLabel(frame63, text="CC Det Abort Interrupt", width = 8,font=("Helvetica", 14))
CC_det_abrt_Intrrpt_Lab.grid(row = 6, column = 0, padx = 7 , pady = 0,sticky = "w")

VSAFE0V_Intrrpt_Lab = ctk.CTkLabel(frame63, text="VFAFE0V Interrupt", width = 8,font=("Helvetica", 14))
VSAFE0V_Intrrpt_Lab.grid(row = 7, column = 0, padx = 7 , pady = 0,sticky = "w")

VCONNOCP_Intrrpt_Lab = ctk.CTkLabel(frame63, text="VCONNOCP Interrupt", width = 8,font=("Helvetica", 14))
VCONNOCP_Intrrpt_Lab.grid(row = 8, column = 0, padx = 7 , pady = 0,sticky = "w")

Inv_lab1 = ctk.CTkLabel(frame63, text="", width = 100)
Inv_lab1.grid(row = 0, column = 1, padx = 7 , pady = 8,sticky = "w")

CC_Intrrpt_Btn_write = ctk.CTkButton(frame63,width = 80, height =10, text = "Write")
CC_Intrrpt_Btn_write.grid(row = 0, column = 2, padx = 10, pady= 1,sticky = "w")

CC_Intrrpt_Btn_read = ctk.CTkButton(frame63,width = 80, height =10, text = "Read")
CC_Intrrpt_Btn_read.grid(row = 0, column = 3, padx = 10, pady= 1,sticky = "w")

CC_Stat_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
CC_Stat_Intrrt_togg_sw.grid(row = 1, column = 1, padx = 20 , pady = 0, sticky = "w")

CC_VCN_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
CC_VCN_Intrrt_togg_sw.grid(row = 2, column = 1, padx = 20 , pady = 0, sticky = "w")

CCIStat_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
CCIStat_Intrrt_togg_sw.grid(row = 3, column = 1, padx = 20 , pady = 0, sticky = "w")

CCPINStat_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
CCPINStat_Intrrt_togg_sw.grid(row = 4, column = 1, padx = 20 , pady = 0, sticky = "w")

Moisture_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
Moisture_Intrrt_togg_sw.grid(row = 5, column = 1, padx = 20 , pady = 0, sticky = "w")

CC_Det_Abrt_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
CC_Det_Abrt_Intrrt_togg_sw.grid(row = 6, column = 1, padx = 20 , pady = 0, sticky = "w")

VSAFE0V_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
VSAFE0V_Intrrt_togg_sw.grid(row = 7, column = 1, padx = 20 , pady = 0, sticky = "w")

VCONNOCP_Intrrt_togg_sw = ctk.CTkSwitch(frame63,width = 100, text="")
VCONNOCP_Intrrt_togg_sw.grid(row = 8, column = 1, padx = 20 , pady = 0, sticky = "w")

################USBC Interrutps######################

CC_Interrupts_Lab = ctk.CTkLabel(frame64, text="USBC Interrupts", width = 10,font=("Helvetica", 14))
CC_Interrupts_Lab.grid(row = 0, column = 0, padx = 7 , pady = 8,sticky = "w")

Attached_hold_Intrrpt_Lab = ctk.CTkLabel(frame64, text="Attached Hold Interrupt", width = 8,font=("Helvetica", 14))
Attached_hold_Intrrpt_Lab.grid(row = 1, column = 0, padx = 7 , pady = 0,sticky = "w")

Charger_Type_Intrrpt_Lab = ctk.CTkLabel(frame64, text="Charger Type Interrupt", width = 8,font=("Helvetica", 14))
Charger_Type_Intrrpt_Lab.grid(row = 2, column = 0, padx = 7 , pady = 0,sticky = "w")

Stop_Mode_Intrrpt_Lab = ctk.CTkLabel(frame64, text="Stop Mode Interrupt", width = 8, font=("Helvetica", 14))
Stop_Mode_Intrrpt_Lab.grid(row = 3, column = 0, padx = 7 , pady = 0,sticky = "w")

DCD_Timer_Intrrpt_Lab = ctk.CTkLabel(frame64, text="DCD Timer Interrupt", width = 8,font=("Helvetica", 14))
DCD_Timer_Intrrpt_Lab.grid(row = 4, column = 0, padx = 7 , pady = 0,sticky = "w")

VBUS_ADC_Intrrpt_Lab = ctk.CTkLabel(frame64, text="VBUS ADC Interrupt", width = 8,font=("Helvetica", 14))
VBUS_ADC_Intrrpt_Lab.grid(row = 5, column = 0, padx = 7 , pady = 0,sticky = "w")

VBUS_Det_Intrrpt_Lab = ctk.CTkLabel(frame64, text="VBUS Det Interrupt", width = 8,font=("Helvetica", 14))
VBUS_Det_Intrrpt_Lab.grid(row = 6, column = 0, padx = 7 , pady = 0,sticky = "w")

USBC_sys_Intrrpt_Lab = ctk.CTkLabel(frame64, text="USBC Sys Mssge Interrupt", width = 8,font=("Helvetica", 14))
USBC_sys_Intrrpt_Lab.grid(row = 7, column = 0, padx = 7 , pady = 0,sticky = "w")

AP_Cmmd_Resp_Interrupt_Lab = ctk.CTkLabel(frame64, text="AP Cmmd Resp Interrupt", width = 8,font=("Helvetica", 14))
AP_Cmmd_Resp_Interrupt_Lab.grid(row = 8, column = 0, padx = 7 , pady = 0,sticky = "w")

Inv_lab2 = ctk.CTkLabel(frame64, text=" ", width = 10)
Inv_lab2.grid(row = 0, column = 1, padx = 40, pady = 8,sticky = "w")

USB_C_Btn_write = ctk.CTkButton(frame64,width = 80, height =10, text = "Write")
USB_C_Btn_write.grid(row = 0, column = 2, padx = 10, pady= 1,sticky = "w")

USB_C_Btn_read = ctk.CTkButton(frame64,width = 80, height =10, text = "Read")
USB_C_Btn_read.grid(row = 0, column = 3, padx = 10, pady= 1,sticky = "w")

Attached_hold_Intrrpt_sw = ctk.CTkSwitch(frame64,width = 220, text="")
Attached_hold_Intrrpt_sw.grid(row = 1, column = 1, padx = 20 , pady = 0, sticky = "w")

Charger_Type_Intrrpt_sw = ctk.CTkSwitch(frame64,width = 220, text="")
Charger_Type_Intrrpt_sw.grid(row = 2, column = 1, padx = 20 , pady = 0, sticky = "w")

Stop_Mode_Intrrpt_sw = ctk.CTkSwitch(frame64,width = 220, text="")
Stop_Mode_Intrrpt_sw.grid(row = 3, column = 1, padx = 20 , pady = 0, sticky = "w")

DCD_Timer_Intrrpt_sw = ctk.CTkSwitch(frame64,width = 220, text="")
DCD_Timer_Intrrpt_sw.grid(row = 4, column = 1, padx = 20 , pady = 0, sticky = "w")

VBUS_ADC_Intrrpt_sw = ctk.CTkSwitch(frame64,width = 220, text="")
VBUS_ADC_Intrrpt_sw.grid(row = 5, column = 1, padx = 20 , pady = 0, sticky = "w")

VBUS_Det_Intrrpt_togg_sw = ctk.CTkSwitch(frame64,width = 220, text="")
VBUS_Det_Intrrpt_togg_sw.grid(row = 6, column = 1, padx = 20 , pady = 0, sticky = "w")

USBC_sys_Intrrpt_togg_sw = ctk.CTkSwitch(frame64,width = 220, text="")
USBC_sys_Intrrpt_togg_sw.grid(row = 7, column = 1, padx = 20 , pady = 0, sticky = "w")

AP_Cmmd_Resp_Interrupt_sw = ctk.CTkSwitch(frame64,width = 220, text="")
AP_Cmmd_Resp_Interrupt_sw.grid(row = 8, column = 1, padx = 20 , pady = 0, sticky = "w")


#frames["BC Control 1 (0x01/0x02)"] = frame1
 


"""tab2"""

# Create a ComboBox in the tab
options = ["Custom Command", "BC Control 1 (0x01/0x02)", "BC Control 2 (0x03/0x04)", "Control 1 (0x05/0x06)","CC Control 1 (0x0B/0x0C)", "CC Control 4 (0x11/0x12)","GPIO Control (0x23/0x24)","GPIO0 GPIO1 ADC (0x27)", "Get SnkCap (0x2F)", "Current SrcCap (0x30)", "Get SrcCap (0x31)", "SrcCap Request (0x32)",
           "Set SrcCap (0x33)", "Send Get Request (0x34)", "Read Get Request (0x35)", "Send Get Response (0x36)", "Send Swap Request (0x37)", "Send Swap Response (0x38)", "SrcCap APDO Request (0x3A)", "Set PPS Mode (0x3C)", "SNK PDO Request (0x3E)", "SNK PDO Set (0x3F)", "Get PD Message (0x4A)", 
           "Custom Configuration (0x55/0x56)", "Master I2C Control (0x85/0x86)"]
combobox = ctk.CTkComboBox(tab2, values=options,command=show_selected_frame, text_color="White", width = 250)
combobox.set("Custom Command")  # set initial value
combobox.place(x = 150, y = 20)




# Create predefined frames with widgets

frame0 = ctk.CTkFrame(tab2, width = 1225, height = 650, border_width=3)
frame0.place(x=150,y= 60)
frame0.pack_propagate(False)
label0 = ctk.CTkLabel(frame0,text='')
#label1.grid(row = 3, column = 0)
label0.pack()
frames["Custom Command"] = frame0


frame1 = ctk.CTkFrame(tab2, width = 1225, height = 650, border_width=3)
frame1.place(x=150,y= 60)
frame1.pack_propagate(False)
label1 = ctk.CTkLabel(frame1, text="This is Frame 1")
#label1.grid(row = 3, column = 0)
label1.pack()
frames["BC Control 1 (0x01/0x02)"] = frame1

frame2 = ctk.CTkFrame(tab2, width = 1225, height = 650, border_width=3)
frame2.place(x=150,y= 60)
frame2.pack_propagate(False)
label2 = ctk.CTkLabel(frame2, text="This is Frame 2")
#label2.grid(row = 3, column = 0)
label2.pack()
frames["BC Control 2 (0x03/0x04)"] = frame2

frame3 = ctk.CTkFrame(tab2,  width = 1225, height = 650, border_width=3)
frame3.place(x=150,y= 60)
frame3.pack_propagate(False)
label3 = ctk.CTkLabel(frame3, text="This is Frame 3")
#label3.grid(row = 3, column = 0)
label3.pack()
frames["Control 1 (0x05/0x06)"] = frame3

frame10 = ctk.CTkFrame(tab2,  width = 1225, height = 650, border_width=3)
frame10.place(x=150,y= 60)
frame10.pack_propagate(False)

Command_data_src_req = ctk.CTkLabel(frame10, text="Command Data", width = 10)
Command_data_src_req.grid(row = 0, column = 0, padx = 10 , pady = 10, sticky = "W")
src_req_Btn = ctk.CTkButton(frame10,width = 100, height =10, text = "Write",command = Curr_src_Cap)
src_req_Btn.grid(row = 0, column = 1, padx = 10, pady= 10,sticky = "E")

No_of_PDOs_sr = ctk.CTkLabel(frame10, text="Number of PDOs", width = 10)
No_of_PDOs_sr.grid(row = 1, column = 0, padx = 10 , pady = 10, sticky = "W")
No_of_PDOs_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
No_of_PDOs_sr_Tb.grid(row = 1, column = 1, padx = 10, pady= 10)

Selected_no_of_PDOs_sr = ctk.CTkLabel(frame10, text="Selected no of PDOs", width = 20)
Selected_no_of_PDOs_sr.grid(row = 2, column = 0, padx = 10 , pady = 10,sticky = "W")
Selected_no_of_PDOs_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
Selected_no_of_PDOs_sr_Tb.grid(row = 2, column = 1, padx = 10, pady= 10)

PDO1_sr = ctk.CTkLabel(frame10, text="PDO1", width = 20)
PDO1_sr.grid(row = 3, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO1_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO1_sr_Tb.grid(row = 3, column = 1, padx = 10, pady= 10)

PDO2_sr = ctk.CTkLabel(frame10, text="PDO2", width = 20)
PDO2_sr.grid(row = 4, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO2_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO2_sr_Tb.grid(row = 4, column = 1, padx = 10, pady= 10)

PDO3_sr = ctk.CTkLabel(frame10, text="PDO3", width = 20)
PDO3_sr.grid(row = 5, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO3_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO3_sr_Tb.grid(row = 5, column = 1, padx = 10, pady= 10)

PDO4_sr = ctk.CTkLabel(frame10, text="PDO4", width = 20)
PDO4_sr.grid(row = 6, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO4_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO4_sr_Tb.grid(row = 6, column = 1, padx = 10, pady= 10)

PDO5_sr = ctk.CTkLabel(frame10, text="PDO5", width = 20)
PDO5_sr.grid(row = 7, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO5_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO5_sr_Tb.grid(row = 7, column = 1, padx = 10, pady= 10)

PDO6_sr = ctk.CTkLabel(frame10, text="PDO6", width = 20)
PDO6_sr.grid(row = 8, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO6_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO6_sr_Tb.grid(row = 8, column = 1, padx = 10, pady= 10)

PDO7_sr = ctk.CTkLabel(frame10, text="PDO7", width = 20)
PDO7_sr.grid(row = 9, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO7_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO7_sr_Tb.grid(row = 9, column = 1, padx = 10, pady= 10)

PDO8_sr = ctk.CTkLabel(frame10, text="PDO8", width = 20)
PDO8_sr.grid(row = 10, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO8_sr_Tb = ctk.CTkTextbox(frame10,width = 1030, height =10)
PDO8_sr_Tb.grid(row = 10, column = 1, padx = 10, pady= 10)

frames["Current SrcCap (0x30)"] = frame10



frame12 = ctk.CTkFrame(tab2,  width = 1225, height = 650, border_width=3)
frame12.place(x=150,y= 60)
frame12.pack_propagate(False)

Command_data_src_cap = ctk.CTkLabel(frame12, text="Command Data", width = 10)
Command_data_src_cap.grid(row = 0, column = 0, padx = 10 , pady = 10, sticky = "W")
src_cap_sc_Btn = ctk.CTkButton(frame12,width = 100, height =10, text = "Write",command=Src_cap_Req)
src_cap_sc_Btn.grid(row = 0, column = 1, padx = 10, pady= 10,sticky = "E")

Req_PDO_Position_sc = ctk.CTkLabel(frame12, text="Number of PDOs", width = 10)
Req_PDO_Position_sc.grid(row = 1, column = 0, padx = 10 , pady = 10, sticky = "W")
Req_PDO_Position_sc_Entry = ctk.CTkEntry(frame12,width = 1030, height =10)
Req_PDO_Position_sc_Entry.insert(0,"0x00")
Req_PDO_Position_sc_Entry.grid(row = 1, column = 1, padx = 10, pady= 10)
frames["SrcCap Request (0x32)"] = frame12



frame21 = ctk.CTkFrame(tab2,  width = 1225, height = 650, border_width=3)
frame21.place(x=150,y= 60)
frame21.pack_propagate(False)

Read_SNK_PDO_sp = ctk.CTkLabel(frame21, text="Read SNK PDO", width = 10)
Read_SNK_PDO_sp.grid(row = 0, column = 0, padx = 10 , pady = 10, sticky = "W")
Read_SNK_PDO_sp_Swh = ctk.CTkSwitch(frame21, text="Memory Write")
Read_SNK_PDO_sp_Swh.grid(row = 0, column = 1, padx = 10 , pady = 10, sticky = "W")
SNK_PDO_req_sp_Btn = ctk.CTkButton(frame21,width = 100, height =10, text = "Write",command=SNK_PDO_REQ)
SNK_PDO_req_sp_Btn.grid(row = 0, column = 1, padx = 10, pady= 10,sticky = "E")

No_of_PDOs_sp = ctk.CTkLabel(frame21, text="Number of PDOs", width = 10)
No_of_PDOs_sp.grid(row = 1, column = 0, padx = 10 , pady = 10, sticky = "W")
No_of_PDOs_sp_Tb = ctk.CTkTextbox(frame21,width = 1030, height =10)
No_of_PDOs_sp_Tb.grid(row = 1, column = 1, padx = 10, pady= 10)

PDO1_sp = ctk.CTkLabel(frame21, text="PDO1", width = 20)
PDO1_sp.grid(row = 2, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO1_sp_Tb = ctk.CTkTextbox(frame21,width = 1030, height =10)
PDO1_sp_Tb.grid(row = 2, column = 1, padx = 10, pady= 10)

PDO2_sp = ctk.CTkLabel(frame21, text="PDO2", width = 20)
PDO2_sp.grid(row = 3, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO2_sp_Tb = ctk.CTkTextbox(frame21,width = 1030, height =10)
PDO2_sp_Tb.grid(row = 3, column = 1, padx = 10, pady= 10)

PDO3_sp = ctk.CTkLabel(frame21, text="PDO3", width = 20)
PDO3_sp.grid(row = 4, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO3_sp_Tb = ctk.CTkTextbox(frame21,width = 1030, height =10)
PDO3_sp_Tb.grid(row = 4, column = 1, padx = 10, pady= 10)

PDO4_sp = ctk.CTkLabel(frame21, text="PDO4", width = 20)
PDO4_sp.grid(row = 5, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO4_sp_Tb = ctk.CTkTextbox(frame21,width = 1030, height =10)
PDO4_sp_Tb.grid(row = 5, column = 1, padx = 10, pady= 10)

PDO5_sp = ctk.CTkLabel(frame21, text="PDO5", width = 20)
PDO5_sp.grid(row = 6, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO5_sp_Tb = ctk.CTkTextbox(frame21,width = 1030, height =10)
PDO5_sp_Tb.grid(row = 6, column = 1, padx = 10, pady= 10)

PDO6_sp = ctk.CTkLabel(frame21, text="PDO6", width = 20)
PDO6_sp.grid(row = 7, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO6_sp_Tb = ctk.CTkTextbox(frame21,width = 1030, height =10)
PDO6_sp_Tb.grid(row = 7, column = 1, padx = 10, pady= 10)

frames["SNK PDO Request (0x3E)"] = frame21





frame22 = ctk.CTkFrame(tab2,  width = 1225, height = 650, border_width=3)
frame22.place(x=150,y= 60)
frame22.pack_propagate(False)

Read_SNK_PDO_ss = ctk.CTkLabel(frame22, text="Write SNK PDO", width = 10)
Read_SNK_PDO_ss.grid(row = 0, column = 0, padx = 10 , pady = 10, sticky = "W")
Read_SNK_PDO_ss_Swh = ctk.CTkSwitch(frame22, text="Memory Write")
Read_SNK_PDO_ss_Swh.grid(row = 0, column = 1, padx = 10 , pady = 10, sticky = "W")
SNK_PDO_req_ss_Btn = ctk.CTkButton(frame22,width = 100, height =10, text = "Write",command =Set_SNK_PDO)
SNK_PDO_req_ss_Btn.grid(row = 0, column = 1, padx = 10, pady= 10,sticky = "E")

No_of_PDOs_ss = ctk.CTkLabel(frame22, text="Number of PDOs", width = 10)
No_of_PDOs_ss.grid(row = 1, column = 0, padx = 10 , pady = 10, sticky = "W")
No_of_PDOs_ss_Etry = ctk.CTkEntry(frame22,width = 1030, height =10)
No_of_PDOs_ss_Etry.insert(0,"0x00")
No_of_PDOs_ss_Etry.grid(row = 1, column = 1, padx = 10, pady= 10)

PDO1_ss = ctk.CTkLabel(frame22, text="PDO1", width = 20)
PDO1_ss.grid(row = 2, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO1_ss_Etry = ctk.CTkEntry(frame22,width = 1030, height =10)
PDO1_ss_Etry.insert(0,"0x00000000")
PDO1_ss_Etry.grid(row = 2, column = 1, padx = 10, pady= 10)

PDO2_ss = ctk.CTkLabel(frame22, text="PDO2", width = 20)
PDO2_ss.grid(row = 3, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO2_ss_Etry = ctk.CTkEntry(frame22,width = 1030, height =10)
PDO2_ss_Etry.insert(0,"0x00000000")
PDO2_ss_Etry.grid(row = 3, column = 1, padx = 10, pady= 10)

PDO3_ss = ctk.CTkLabel(frame22, text="PDO3", width = 20)
PDO3_ss.grid(row = 4, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO3_ss_Etry = ctk.CTkEntry(frame22,width = 1030, height =10)
PDO3_ss_Etry.insert(0,"0x00000000")
PDO3_ss_Etry.grid(row = 4, column = 1, padx = 10, pady= 10)

PDO4_ss = ctk.CTkLabel(frame22, text="PDO4", width = 20)
PDO4_ss.grid(row = 5, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO4_ss_Etry = ctk.CTkEntry(frame22,width = 1030, height =10)
PDO4_ss_Etry.insert(0,"0x00000000")
PDO4_ss_Etry.grid(row = 5, column = 1, padx = 10, pady= 10)

PDO5_ss = ctk.CTkLabel(frame22, text="PDO5", width = 20)
PDO5_ss.grid(row = 6, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO5_ss_Etry = ctk.CTkEntry(frame22,width = 1030, height =10)
PDO5_ss_Etry.insert(0,"0x00000000")
PDO5_ss_Etry.grid(row = 6, column = 1, padx = 10, pady= 10)

PDO6_ss = ctk.CTkLabel(frame22, text="PDO6", width = 20)
PDO6_ss.grid(row = 7, column = 0, padx = 10 , pady = 10,sticky = "W")
PDO6_ss_Etry = ctk.CTkEntry(frame22,width = 1030, height =10)
PDO6_ss_Etry.insert(0,"0x00000000")
PDO6_ss_Etry.grid(row = 7, column = 1, padx = 10, pady= 10)

frames["SNK PDO Set (0x3F)"] = frame22

'''tab3'''

frame_quick_run_1 = ctk.CTkFrame(tab3, width=610, height=515, border_width=3)
frame_quick_run_1.grid(row=0, column=0, padx=100, pady=20, sticky = "NW")
frame_quick_run_1.grid_propagate(False)

frame_quick_run_2 = ctk.CTkFrame(tab3, width=610, height=515, border_width=3)
frame_quick_run_2.grid(row=0, column=0, padx=750, pady=20, sticky = "NW")
frame_quick_run_2.grid_propagate(False)

#######Status#######

USB_C_Status_Label = ctk.CTkLabel(frame_quick_run_1, text="Type of Source Connected", width = 20,font=("Helvetica", 14))
USB_C_Status_Label.grid(row = 0, column = 0, padx = 20 , pady = 3,sticky = "W")

Status_Read_Btn = ctk.CTkButton(frame_quick_run_1,width = 80, height =10, text = "Read",command=Check_Status)
Status_Read_Btn.grid(row = 0, column = 0, padx = 23, pady= 10,sticky = "e")

frame_quick_run_1_1 = ctk.CTkFrame(frame_quick_run_1, width=570, height=450, border_width=3)
frame_quick_run_1_1.grid(row=1, column=0, padx=20, pady=0, sticky = "NE")
frame_quick_run_1_1.grid_propagate(False) 


VBUS_ADC_Label = ctk.CTkLabel(frame_quick_run_1_1, text="VBUS ADC", width = 20,font=("Helvetica", 14))
VBUS_ADC_Label.grid(row = 0, column = 0, padx = 10 , pady = 3,sticky = "W")

Charger_Detec_Label = ctk.CTkLabel(frame_quick_run_1_1, text="Charger Detection Status", width = 20,font=("Helvetica", 14))
Charger_Detec_Label.grid(row = 1, column = 0, padx = 10 , pady = 3,sticky = "W")

VBUS_Detec_Label = ctk.CTkLabel(frame_quick_run_1_1, text="VBUS Detection Status", width = 20,font=("Helvetica", 14))
VBUS_Detec_Label.grid(row = 2, column = 0, padx = 10 , pady = 3,sticky = "W")

CC_Pin_state_mac_det = ctk.CTkLabel(frame_quick_run_1_1, text="CC Pin State M/c det", width = 20,font=("Helvetica", 14))
CC_Pin_state_mac_det.grid(row = 3, column = 0, padx = 10 , pady = 3,sticky = "W")

CC_Pin_det_max_ct = ctk.CTkLabel(frame_quick_run_1_1, text="CC Pin Det Current", width = 20,font=("Helvetica", 14))
CC_Pin_det_max_ct.grid(row = 4, column = 0, padx = 10 , pady = 3,sticky = "W")

Active_cc_pin_label = ctk.CTkLabel(frame_quick_run_1_1, text="Active CC Pin", width = 20,font=("Helvetica", 14))
Active_cc_pin_label.grid(row = 5, column = 0, padx = 10 , pady = 3,sticky = "W")

VSAFE0V_status_label = ctk.CTkLabel(frame_quick_run_1_1, text="VSAFE0V_Status", width = 20,font=("Helvetica", 14))
VSAFE0V_status_label.grid(row = 6, column = 0, padx = 10 , pady = 3,sticky = "W")

PD_Message_label = ctk.CTkLabel(frame_quick_run_1_1, text="PD Message", width = 20,font=("Helvetica", 14))
PD_Message_label.grid(row = 7, column = 0, padx = 10 , pady = 3,sticky = "W")

PSRDY_Status_label = ctk.CTkLabel(frame_quick_run_1_1, text="PSRDY Status", width = 20,font=("Helvetica", 14))
PSRDY_Status_label.grid(row = 8, column = 0, padx = 10 , pady = 3,sticky = "W")

Power_Role_label = ctk.CTkLabel(frame_quick_run_1_1, text="Power Role", width = 20,font=("Helvetica", 14))
Power_Role_label.grid(row = 9, column = 0, padx = 10 , pady = 3,sticky = "W")

Data_Role_label = ctk.CTkLabel(frame_quick_run_1_1, text="Data Role", width = 20,font=("Helvetica", 14))
Data_Role_label.grid(row = 10, column = 0, padx = 10 , pady = 3,sticky = "W")



VBUS_ADC_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
VBUS_ADC_Tb.grid(row = 0, column = 1, padx = 10, pady= 5)

Charger_Detec_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
Charger_Detec_Tb.grid(row = 1, column = 1, padx = 10, pady= 5)

VBUS_Detec_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
VBUS_Detec_Tb.grid(row = 2, column = 1, padx = 10, pady= 5)

CC_Pin_state_mac_det_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
CC_Pin_state_mac_det_Tb.grid(row = 3, column = 1, padx = 10, pady= 5)

CC_Pin_det_max_ct_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
CC_Pin_det_max_ct_Tb.grid(row = 4, column = 1, padx = 10, pady= 5)

Active_cc_pin_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
Active_cc_pin_Tb.grid(row = 5, column = 1, padx = 10, pady= 5)

VSAFE0V_status_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
VSAFE0V_status_Tb.grid(row = 6, column = 1, padx = 10, pady= 5)

PD_Message_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
PD_Message_Tb.grid(row = 7, column = 1, padx = 10, pady= 5)

PSRDY_Status_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
PSRDY_Status_Tb.grid(row = 8, column = 1, padx = 10, pady= 5)

Power_Role_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
Power_Role_Tb.grid(row = 9, column = 1, padx = 10, pady= 5)

Data_Role_Tb = ctk.CTkTextbox(frame_quick_run_1_1,width = 370, height =0)
Data_Role_Tb.grid(row = 10, column = 1, padx = 10, pady= 5)

###Source PDO Settings

Src_PDO_Settings_Label = ctk.CTkLabel(frame_quick_run_2, text="Choose from available PDOs", width = 20,font=("Helvetica", 14))
Src_PDO_Settings_Label.grid(row = 0, column = 0, padx = 20 , pady = 3,sticky = "W")

Src_PDO_Settings_Btn_Read = ctk.CTkButton(frame_quick_run_2,width = 80, height =10, text = "Read",command=Read_Quick_PDO_Voltage)
Src_PDO_Settings_Btn_Read.grid(row = 0, column = 0, padx = 120, pady= 10,sticky = "e")

Src_PDO_Settings_Btn_write = ctk.CTkButton(frame_quick_run_2,width = 80, height =10, text = "Write",command=Set_Quick_PDO_Voltage)
Src_PDO_Settings_Btn_write.grid(row = 0, column = 0, padx = 25, pady= 10,sticky = "e")


frame_quick_run_2_1 = ctk.CTkFrame(frame_quick_run_2, width=570, height=130, border_width=3)
frame_quick_run_2_1.grid(row=1, column=0, padx=20, pady=0, sticky = "NE")
frame_quick_run_2_1.grid_propagate(False) 



No_of_PDOs_quick_run_Label = ctk.CTkLabel(frame_quick_run_2_1, text="No of PDOs", width = 20,font=("Helvetica", 14))
No_of_PDOs_quick_run_Label.grid(row = 0, column = 0, padx = 10 , pady = 3,sticky = "W")

Curr_PDO_Pos_quick_Label = ctk.CTkLabel(frame_quick_run_2_1, text="Current PDO Position", width = 20,font=("Helvetica", 14))
Curr_PDO_Pos_quick_Label.grid(row = 1, column = 0, padx = 10 , pady = 3,sticky = "W")

Set_PDO_Pos_quick_Label = ctk.CTkLabel(frame_quick_run_2_1, text="Set PDO Position", width = 20,font=("Helvetica", 14))
Set_PDO_Pos_quick_Label.grid(row = 2, column = 0, padx = 10 , pady = 3,sticky = "W")


No_of_PDOs_quick_run_Tb = ctk.CTkTextbox(frame_quick_run_2_1,width = 390, height =0)
No_of_PDOs_quick_run_Tb.grid(row = 0, column = 1, padx = 10, pady= 5)

Curr_PDO_Pos_quick_Tb = ctk.CTkTextbox(frame_quick_run_2_1,width = 390, height =0)
Curr_PDO_Pos_quick_Tb.grid(row = 1, column = 1, padx = 10, pady= 5)

Set_PDO_quick_combo = ctk.CTkComboBox(frame_quick_run_2_1, values = ['Not available'], text_color="White", width = 390)
Set_PDO_quick_combo.set("Please press the Read button")  # set initial value
Set_PDO_quick_combo.grid(row = 2, column = 1, padx = 10, pady= 5)
#Set_PDO_quick_combo.bind("<<ComboboxSelected>>",)


#############Charger Settings###############
frame_quick_run_3 = ctk.CTkFrame(tab3, width=1260, height=175, border_width=3)
frame_quick_run_3.grid(row=1, column=0, padx=100, pady=5, sticky = "W")
frame_quick_run_3.grid_propagate(False)

Charger_Settings_Label = ctk.CTkLabel(frame_quick_run_3, text="Charger Settings (MAX77986A)", width = 20,font=("Helvetica", 14))
Charger_Settings_Label.grid(row = 0, column = 0, padx = 20 , pady = 3,sticky = "W")

Char_sett_Write_Btn = ctk.CTkButton(frame_quick_run_3,width = 80, height =10, text = "Write",command=Initialize_Charger)
Char_sett_Write_Btn.grid(row = 0, column = 0, padx = 23, pady= 10,sticky = "e")

frame_quick_run_3_1 = ctk.CTkFrame(frame_quick_run_3, width=1220, height=115, border_width=3)
frame_quick_run_3_1.grid(row=1, column=0, padx=20, pady=0, sticky = "NE")
frame_quick_run_3_1.grid_propagate(False) 



Chg_term_vg_Label = ctk.CTkLabel(frame_quick_run_3_1, text="Charge Termination Voltage", width = 20,font=("Helvetica", 14))
Chg_term_vg_Label.grid(row = 0, column = 0, padx = 10 , pady = 3,sticky = "W")

Charger_input_current_Label = ctk.CTkLabel(frame_quick_run_3_1, text="CHGIN Input Current Limit", width = 20,font=("Helvetica", 14))
Charger_input_current_Label.grid(row = 1, column = 0, padx = 10 , pady = 3,sticky = "W")

Fast_Charge_Label = ctk.CTkLabel(frame_quick_run_3_1, text="Fast Charge Current Selectn.", width = 20,font=("Helvetica", 14))
Fast_Charge_Label.grid(row = 2, column = 0, padx = 10 , pady = 3,sticky = "W")

Chg_term_vg_Tb = ctk.CTkTextbox(frame_quick_run_3_1,width = 100, height =0)
Chg_term_vg_Tb.grid(row = 0, column = 1, padx = 10 , pady = 3,sticky = "W")

Charger_input_current_Tb =  ctk.CTkTextbox(frame_quick_run_3_1,width = 100, height =0)
Charger_input_current_Tb.grid(row = 1, column = 1, padx = 10 , pady = 3,sticky = "W")

Fast_Charge_Tb =  ctk.CTkTextbox(frame_quick_run_3_1,width = 100, height =0)
Fast_Charge_Tb.grid(row = 2, column = 1, padx = 10 , pady = 3,sticky = "W")

Chg_term_vg_unit_Label = ctk.CTkLabel(frame_quick_run_3_1, text="V", width = 20,font=("Helvetica", 14))
Chg_term_vg_unit_Label.grid(row = 0, column = 2, padx = 0 , pady = 3,sticky = "W")

Charger_input_current_unit_Label = ctk.CTkLabel(frame_quick_run_3_1, text="A", width = 20,font=("Helvetica", 14))
Charger_input_current_unit_Label.grid(row = 1, column = 2, padx = 0 , pady = 3,sticky = "W")

Fast_Charge_unit_Label = ctk.CTkLabel(frame_quick_run_3_1, text="A", width = 20,font=("Helvetica", 14))
Fast_Charge_unit_Label.grid(row = 2, column = 2, padx = 0 , pady = 3,sticky = "W")

Chg_term_vg_slider = ctk.CTkSlider(frame_quick_run_3_1, from_=0, to=31, number_of_steps= 31, width = 830, command = Charge_Termiantn_Volt_Set)
Chg_term_vg_slider.grid(row = 0, column = 3, padx = 20 , pady = 3,sticky = "W")

Charger_input_current_slider = ctk.CTkSlider(frame_quick_run_3_1, from_=0, to=109,number_of_steps= 109,width = 830,command=Charge_Termiantn_chg_lct_lim_Set)
Charger_input_current_slider.grid(row = 1, column = 3, padx = 20 , pady = 3,sticky = "W")

Fast_Charge_slider = ctk.CTkSlider(frame_quick_run_3_1, from_=0, to=110, number_of_steps= 110, width = 830,command=Charge_Termiantn_fast_lim_Set)
Fast_Charge_slider.grid(row = 2, column = 3, padx = 20 , pady = 3,sticky = "W")


#########Setting Initial Voltage Plugin/Sink PDO Setting##########

Set_Sink_PDO_quick_Label = ctk.CTkLabel(frame_quick_run_2, text="Sink PDO Setting", width = 20,font=("Helvetica", 14))
Set_Sink_PDO_quick_Label.grid(row = 2, column = 0, padx = 20 , pady = 3,sticky = "W")

Set_Sink_PDO_quick_Btn_write = ctk.CTkButton(frame_quick_run_2,width = 80, height =10, text = "Write", command = Set_Plugin_Initial_Voltage)
Set_Sink_PDO_quick_Btn_write.grid(row = 2, column = 0, padx = 25, pady= 10,sticky = "e")

frame_quick_run_2_2 = ctk.CTkFrame(frame_quick_run_2, width=570, height=50, border_width=3)
frame_quick_run_2_2.grid(row=3, column=0, padx=20, pady=0, sticky = "NE")
frame_quick_run_2_2.grid_propagate(False)

Set_Plug_in_volt_init_Label = ctk.CTkLabel(frame_quick_run_2_2, text="Choose Initial Voltage", width = 20,font=("Helvetica", 14))
Set_Plug_in_volt_init_Label.grid(row = 0, column = 0, padx = 10 , pady = 10,sticky = "W")

Initial_Voltage_Combo = ctk.CTkComboBox(frame_quick_run_2_2, values = ['5V/3A', '9V/3A', '15V/3A'], text_color="White", width = 390)
Initial_Voltage_Combo.set("Select Voltage")  # set initial value
Initial_Voltage_Combo.grid(row = 0, column = 1, padx = 10, pady= 10)

###################PPS Mode for Fast charging######################

PPS_Mode_Label = ctk.CTkLabel(frame_quick_run_2, text="PPS Mode", width = 20,font=("Helvetica", 14))
PPS_Mode_Label.grid(row = 4, column = 0, padx = 20 , pady = 3,sticky = "W")

PPS_Mode_quick_Btn_write = ctk.CTkButton(frame_quick_run_2,width = 80, height =10, text = "Write", command = Set_PPS_Mode_Volt_Curr)
PPS_Mode_quick_Btn_write.grid(row = 4, column = 0, padx = 25, pady= 10,sticky = "E")

frame_quick_run_2_3 = ctk.CTkFrame(frame_quick_run_2, width=570, height=183, border_width=3)
frame_quick_run_2_3.grid(row=5, column=0, padx=20, pady=0, sticky = "NE")
frame_quick_run_2_3.grid_propagate(False)

PPS_Enable_Label = ctk.CTkLabel(frame_quick_run_2_3, text="Enable PPS Mode", width = 20,font=("Helvetica", 14))
PPS_Enable_Label.grid(row = 0, column = 0, padx = 10 , pady = 4,sticky = "W")

PPS_Enable_togg_sw = ctk.CTkSwitch(frame_quick_run_2_3,width = 20, text="")
PPS_Enable_togg_sw.grid(row = 0, column = 1, padx = 20 , pady = 0, sticky = "w")

PPS_Sel_APDO_Pos_Label = ctk.CTkLabel(frame_quick_run_2_3, text="Select APDO", width = 20,font=("Helvetica", 14))
PPS_Sel_APDO_Pos_Label.grid(row = 1, column = 0, padx = 10 , pady = 3,sticky = "W")

PPS_Volt_Label = ctk.CTkLabel(frame_quick_run_2_3, text="PPS Voltage", width = 20,font=("Helvetica", 14))
PPS_Volt_Label.grid(row = 2, column = 0, padx = 10 , pady = 3,sticky = "W")

PPS_curr_Label = ctk.CTkLabel(frame_quick_run_2_3, text="PPS Current", width = 20,font=("Helvetica", 14))
PPS_curr_Label.grid(row = 3, column = 0, padx = 10 , pady = 3,sticky = "W")

Select_APDO_Combo = ctk.CTkComboBox(frame_quick_run_2_3, values = ['Position 1', 'Position 2', 'Position 3', 'Position 4', 'Position 5', 'Position 6', 'Position 7', 'Position 8'], text_color="White", width = 400)
Select_APDO_Combo.set("Select")  # set initial value
Select_APDO_Combo.grid(row = 1, column = 1, padx = 20, pady= 5,sticky = 'w')

PPS_Volt_slider = ctk.CTkSlider(frame_quick_run_2_3, from_=0, to=1000, number_of_steps= 200, width = 405, command =Display_PPS_Voltage)
PPS_Volt_slider.grid(row = 2, column = 1, padx = 20 , pady = 3,sticky = "W")

PPS_curr_slider = ctk.CTkSlider(frame_quick_run_2_3, from_=0, to=124, number_of_steps= 124, width = 405, command = Display_PPS_Current)
PPS_curr_slider.grid(row = 3, column = 1, padx = 20 , pady = 3,sticky = "W")

PPS_volt_Tb =  ctk.CTkTextbox(frame_quick_run_2_3,width = 100, height =0)
PPS_volt_Tb.grid(row = 4, column = 1, padx = 20 , pady = 3,sticky = "W")

PPS_mV_Label = ctk.CTkLabel(frame_quick_run_2_3, text="V", width = 10,font=("Helvetica", 14))
PPS_mV_Label.grid(row = 4, column = 1, padx = 130 , pady = 3,sticky = "W")

PPS_curr_Tb =  ctk.CTkTextbox(frame_quick_run_2_3,width = 100, height =0)
PPS_curr_Tb.grid(row = 4, column = 1, padx = 160, pady = 3,sticky = "W")

PPS_mA_Label = ctk.CTkLabel(frame_quick_run_2_3, text="A", width = 10,font=("Helvetica", 14))
PPS_mA_Label.grid(row = 4, column = 1, padx = 270 , pady = 3,sticky = "W")



"""tab 4"""

frame_quick_run_4 = ctk.CTkFrame(tab4, width=1260, height=140, border_width=3)
frame_quick_run_4.grid(row=0, column=0, padx=100, pady=5, sticky = "W")
frame_quick_run_4.grid_propagate(False)

OTG_Settings_Label = ctk.CTkLabel(frame_quick_run_4, text="OTG Settings (MAX77986A)", width = 20,font=("Helvetica", 14))
OTG_Settings_Label.grid(row = 0, column = 0, padx = 20 , pady = 3,sticky = "W")

OTG_sett_Write_Btn = ctk.CTkButton(frame_quick_run_4,width = 80, height =10, text = "Write", command = Reverse_OTG_Mode)
OTG_sett_Write_Btn.grid(row = 0, column = 0, padx = 23, pady= 10,sticky = "e")

frame_quick_run_4_1 = ctk.CTkFrame(frame_quick_run_4, width=1220, height=90, border_width=3)
frame_quick_run_4_1.grid(row=1, column=0, padx=20, pady=0, sticky = "NE")
frame_quick_run_4_1.grid_propagate(False) 



Reverse_voltage_Label = ctk.CTkLabel(frame_quick_run_4_1, text="BYP Voltage", width = 20,font=("Helvetica", 14))
Reverse_voltage_Label.grid(row = 0, column = 0, padx = 10 , pady = 6,sticky = "W")

Rev_curr_limit_Label = ctk.CTkLabel(frame_quick_run_4_1, text="CHGIN Output Current Limit", width = 20,font=("Helvetica", 14))
Rev_curr_limit_Label.grid(row = 1, column = 0, padx = 10 , pady = 3,sticky = "W")

Reverse_voltage_Tb = ctk.CTkTextbox(frame_quick_run_4_1,width = 100, height =0)
Reverse_voltage_Tb.grid(row = 0, column = 1, padx = 10 , pady = 3,sticky = "W")

Rev_curr_limit_Tb =  ctk.CTkTextbox(frame_quick_run_4_1,width = 100, height =0)
Rev_curr_limit_Tb.grid(row = 1, column = 1, padx = 10 , pady = 3,sticky = "W")

Rev_volt_unit_Label = ctk.CTkLabel(frame_quick_run_4_1, text="V", width = 20,font=("Helvetica", 14))
Rev_volt_unit_Label.grid(row = 0, column = 2, padx = 0 , pady = 3,sticky = "W")

Rev_curr_lim_unit_Label = ctk.CTkLabel(frame_quick_run_4_1, text="A", width = 20,font=("Helvetica", 14))
Rev_curr_lim_unit_Label.grid(row = 1, column = 2, padx = 0 , pady = 3,sticky = "W")


Reverse_voltage_slider = ctk.CTkSlider(frame_quick_run_4_1, from_=0, to=70, number_of_steps= 70, width = 830, command = Display_OTG_Voltage)
Reverse_voltage_slider.grid(row = 0, column = 3, padx = 20 , pady = 3,sticky = "W")

Reverse_current_limit_slider = ctk.CTkSlider(frame_quick_run_4_1, from_=0, to=26,number_of_steps= 26,width = 830, command = Display_OTG_Current)
Reverse_current_limit_slider.grid(row = 1, column = 3, padx = 20 , pady = 3,sticky = "W")


    
# Initially hide frame1, frame2, and frame3
frame1.place_forget()
frame2.place_forget()
frame3.place_forget()
frame10.place_forget()
frame12.place_forget()
frame21.place_forget()
frame22.place_forget()


#start serial port
s = sr.Serial('COM8',115200); #always set this before starting
s.reset_input_buffer()


root.mainloop()
