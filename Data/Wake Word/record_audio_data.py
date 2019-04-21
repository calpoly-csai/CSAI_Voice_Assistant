# -----------
# Part 1
# -----------

quit_inp = 0
while (quit_inp != 'q'):    
        feat_type = 0
        gender = 0
        end_desc_sess = 0

        while not(feat_type == "ww" or feat_type == "notww"):
                feat_type = input("WW or NotWW: ").lower()

        if (feat_type == "ww"):
                target_dir = "Wake Word"
                first_name = input("First Name: ").lower()
                last_name = input("Last Name: ").lower()
                ww_descr = input("Enter the description: ").lower()
                ww_loc = input("Location: ").lower()

                while not (gender == "male" or gender == "female"):
                        gender = input("Male or Female: ").lower()

        else:
                target_dir = "Not Wake Word"
                nww_descr = input("Enter description: ")
                nww_loc = input("Location: ").lower()

        while (end_desc_sess != 'e'):
                
                # ----------
                # Part 2
                # ----------

                end_desc_sess = input("If end of description session, type (e); otherwise, type anything else: ").lower()

        quit_inp = input("If finished recording, type (q). Otherwise, type anything else: ").lower()