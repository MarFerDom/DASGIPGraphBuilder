
      function clear_graphs(){
        // Get the image frame
        let img_frame = document.getElementById("img")
        // Clear the frame
        img_frame.textContent = '';
      }
      
      // Function that requests the graphs and place them in website
      async function request_graph(options){
        document.getElementById("loader").style.display = "block";
        await Promise.all(options["files"].map(async (file) => {
          let file_option = {"files":[file], "sources":options["sources"]}
          let opt = {method: "POST", body: JSON.stringify(file_option),
                      headers: {"Content-Type": "application/json"}};
          // Call the API to generate the graphs and use list of file names to add graphs to website.
          let url = document.getElementById("main").dataset.graphUrl;
          await fetch(url, opt)
          .then((response) => response.json())
          .then((data) => {
            // Get the image frame
            let img_frame = document.getElementById("img")
            // Create new image
            data["paths"].forEach((path) => {
              // Set a title
              let title = document.createElement("p")
              title.textContent = path;
              img_frame.appendChild(title);
              // Break line
              img_frame.appendChild(document.createElement("br"));
              // Create new image
              let img = document.createElement("img");
              img.src = document.getElementById("main").dataset.imgUrl+path;
              img.alt = path
              img.style = "width:1024px;";
              img_frame.appendChild(img);
            });
          });
        }));
      }
      
      // Get all checkboxes for source selection
      const source_selection = document.querySelectorAll(".source_selection input[type='checkbox']");
      // Get all checkboxes for variable selection
      const vars_selection = document.querySelectorAll(".vars_selection input[type='checkbox']");
      
      // Object to store graph configurations.
      const data = {};
      
      // Function to update graph configurations object with current selection.
      function update_config(){
        let options_config = {};
        vars_selection.forEach((checkbox) => {
          if (checkbox.checked) {
            let color = document.getElementsByName(checkbox.name + "_color")[0].value;
            let min = document.getElementsByName(checkbox.name + "_min")[0].value;
            let max = document.getElementsByName(checkbox.name + "_max")[0].value;
            options_config[checkbox.name] = [color, min, max];
          }
          //else delete options[checkbox.id];
        });
        let opt = {method: "POST", body: JSON.stringify(options_config), headers: {"Content-Type": "application/json"}};
        // Call the API to change the configuration.
        let url = document.getElementById("main").dataset.configUrl;
        fetch(url, opt)
        .then(response => {
          if(!response.ok) alert("Error: "+response.status);
        });
      }
      
      // Function to update the selected sources [DUMMY: IMPLEMENT THIS FUNCTION]
      function get_sources(){
        let sources = [];
        source_selection.forEach((checkbox) => {
          if (checkbox.checked) {
            sources.push(checkbox.id);
          }
        });
        data["sources"] = sources;
      }
      
      // Function to get selected files [DUMMY: IMPLEMENT THIS FUNCTION]
      function get_files(){
        let select = document.getElementById("file_select");
        let options = select && select.options;
        let selected_files = [];
        for(let i in options){
          if(options[i].selected){
            selected_files.push(options[i].value);
          }
        }
        data["files"] = selected_files;
      }
      
      function send_request(){
        // Update graph configuration
        update_config();
        // Get files
        get_files();
        // Get sources
        get_sources();
      
        if(data["files"].length == 0) {
          alert("No file selected !");
        } else if(data["sources"].length == 0) {
          alert("No sources selected !");
        } else {
          request_graph(data).then(() => {
            document.getElementById("loader").style.display = "none";
          });
        }
      }
      
      // topnav
      function openNav() {
        document.getElementById("myNav").style.width = "100%";
      }
      
      /* Close when someone clicks on the "x" symbol inside the overlay */
      function closeNav() {
        document.getElementById("myNav").style.width = "0%";
      }
      
      
      /* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
      function myFunction() {
        var x = document.getElementById("myTopnav");
        if (x.className === "topnav") {
          x.className += " responsive";
        } else {
          x.className = "topnav";
        }
      }
      
      // sidebar
      function openNavFiles() {
        document.getElementById("navFiles").style.width = "400px";
        document.getElementById("main").style.marginRight = "400px";
      }
      
      /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
      function closeNavFiles() {
        document.getElementById("navFiles").style.width = "0";
        document.getElementById("main").style.marginRight = "0";
      }
      