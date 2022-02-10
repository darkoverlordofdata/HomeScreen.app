            
            
            
        copyright = dis.read_line(null);
        title = dis.read_line(null);
            
        var copy1 = copyright.substring(0, copyright.index_of("("));
        var copy2 = copyright.substring(copyright.index_of("(")+2);

        /* Load the descriptive text */
        try {
            if (parms.verbosity > 1) { 
                print(@"filename: $textfn\n");
            }
            var file = File.new_for_path(textfn);
            if (file.query_exists ()) {
                var dis = new DataInputStream (file.read ());
                copyright = dis.read_line(null);
                title = dis.read_line(null);
            }
    
        }
        catch (Error e) {}
        
        //...
        // xftdrawstring
        drawable.draw_string_utf8(&color, font_16, 60,  60, title, title.length);
        drawable.draw_string_utf8(&color, font_12, 60,  85, copy1, copy1.length);
        drawable.draw_string(&color, font_08, 60, 110, copy2, copy2.length-1);
