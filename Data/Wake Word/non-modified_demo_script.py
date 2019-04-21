# ================================
# PART ONE OF CODING PRESENTATION
# Delete this comment and insert
# code here
# ================================

quit_inp = 0 # var for quitting out of program

# program loop
while (quit_inp != 'q'):    
        feat_type = 0 # wake or not wake work label
        gender = 0 # gender label
        end_desc_sess = 0 # ends the current description session

        # ensures proper input of either ww or notww
        while not(feat_type == "ww" or feat_type == "notww"): 
                feat_type = input("WW or NotWW: ").lower()

        if (feat_type == "ww"):
                target_dir = "Wake Word" # used for setting the correct directory
                ww_noise = 0
                first_name = input("First Name: ").lower() # used for labeling file
                last_name = input("Last Name: ").lower() # ''

                # ensures proper input
                while not (gender == "m" or gender == "f"):
                        gender = input("Male (m) or Female (f): ").lower()

                ww_descr = (input("Enter the description: ").lower()).replace(" ","_") # labeling brief description
                ww_loc = (input("Location: ").lower()).replace(" ","_") # labeling the recording location

                while not(ww_noise == 'q' or ww_noise == 'm' or ww_noise == 'l'):
                        ww_noise = input("Noise Level - Quiet (Q) Moderate (M) Loud (L): ").lower()

        else:
                target_dir = "Not Wake Word"
                nww_noise = 0
                nww_descr = ((input("Enter description: ")).lower()).replace(" ","_")
                nww_loc = (input("Location: ").lower()).replace(" ","_")
                
                while not(nww_noise == 'q' or nww_noise == 'm' or nww_noise == 'l'):
                        nww_noise = input("Noise Level - Quiet (Q) Moderate (M) Loud (L): ").lower()

        # description session loop
        while (end_desc_sess != 'e'):

                # ================================
                # PART TWO OF CODING PRESENTATION
                # Delete this comment and insert
                # code here
                # ================================

                end_desc_sess = input("If finished with description session, type (e); otherwise, type anything else: ").lower()

        quit_inp = input("If finished recording, type (q). Otherwise, type anything else: ").lower()