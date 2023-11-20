// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.
//import styles from './style.css' 
function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function getTime(){
  var dt = new Date();
  var dt_str =  dt.getFullYear()+"-"
  +(dt.getMonth()+1)+"-"
  +dt.getDate()+" "
  +dt.getHours() + ":"
  +dt.getMinutes() + ":" 
  +dt.getSeconds() + "."
  +String(dt.getMilliseconds()).padStart(3, "0");
  return dt_str
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  if (!window.rendered) {
    // You most likely want to get the data passed in like this
    // const {input1, input2, input3} = event.detail.args
    // values format --> dict {Ziel:[Filenamen]}
    const {values, comp_height, key} = event.detail.args
    window.output = {}
    console.warn(document.body.offsetWidth)
    const goal_width_base = document.body.offsetWidth/(Object.keys(values).length +1)
    console.warn(goal_width_base)
    window.selected_div = " "
    var g = 0

    for ( const [key, val_lst] of Object.entries(values)){
      // draw all files of category
      for ( i=0; i < val_lst.length; i++){
        // define container for image and text 
        var div = document.createElement("div")
        div.id = String(g)+"_"+String(i)
        div.classList.add("datei_container")
        div.style.left = String(Math.round(Math.random() * (document.body.offsetWidth*.95)))+"px"//String(Math.round(i * 100))+"px"
        div.style.top = String(Math.round(Math.random() *  window.frames.innerHeight*.3))+"px"//"0px"
        div.style.height = "50px"
        div.style.width = "50px"
        // add container selection
        div.addEventListener("mouseup", function(){
          if (window.selected_div!=" "){
            //window.selected_div.style.top = String(Math.min(window.frameElement.height-parseInt(window.selected_div.style.height),Math.max(0,event.clientY - parseInt(window.selected_div.style.height)/2))) + 'px';
            //window.selected_div.style.left = Math.min(window.frameElement.width-parseInt(window.selected_div.style.width),Math.max(0,event.clientX - parseInt(window.selected_div.style.width)/2)) + 'px';
            var last_selected = document.getElementById(window.selected_div)
            last_selected.style.borderStyle = "none"
          } 
          this.style.borderStyle = "solid"
          window.selected_div = this.id
        })
        
        // define image
        img = document.createElement('img')
        img.src = "./Datei.png"
        img.classList.add("datei_img")
        
        // define text 
        file_name = document.createElement('div')
        file_name.classList.add("datei_name")
        file_name.innerHTML += String(val_lst[i])

        // append elements to container
        div.appendChild(img)
        div.appendChild(file_name)

        // initial entry in logging for container 
        window.output[div.id] = [
          {
            "time":getTime(),
            "x":div.style.left,
            "y":div.style.top,
            "overlap":false
          }]

        // add container to component 
        document.body.appendChild(div)
      }

      // defining endlocation
      var goal = document.createElement("div")
      goal.id = "goal_"+String(g)
      goal.classList.add('goal')

      // add dynamic elements 
      goal.innerHTML += "Bitte hier klicken um "+String(key)+" ablegen"//"stuff"//style.backroundColor="red"
      goal.style.width = String(parseInt(document.body.offsetWidth)*.2) + "px"//Math.floor(goal_width_base/100)*100+"px"//
      goal.style.height = window.screen.height * .2 +"px"
      goal.style.top = goal.style.bottom - goal.style.height
      goal.style.left = String(((g+1)) * parseInt(goal_width_base) -parseInt(goal.style.width)/2)+"px"
      
      // add component movement from and to goal
      //goal.addEventListener("mouseup", function(event){
      goal.addEventListener("mouseup", function(event){
        if (window.selected_div != " "){
          console.warn(window)
          // change location of movable div
          var moving_div = document.getElementById(window.selected_div)
          console.warn(moving_div.getAttribute("height"))
          //console.warn(this.style.left)
          //console.warn(window.selected_div)
          //console.warn(moving_div.style.width)
          //moving_div.style.top = String(parseInt(parseFloat(window.screen.height)*comp_height)-(parseInt(this.style.height))+parseInt(moving_div.id.charAt(0)+1)*2 + 40) +"px"
          //moving_div.style.left = String(parseInt(this.style.left) + parseInt(moving_div.id.split("_").pop()+ 1)*12 +20)+"px"//String(parseInt(this.style.left) + Math.floor(Math.random() * (parseInt(this.style.width)*.8  + 1)))+"px"
          console.warn(Math.max(0,event.clientY - parseInt(moving_div.style.height)/2))
          console.warn(event.screenX)
          console.warn(parseInt(moving_div.style.height)/2)
          console.warn(String(Math.min(window.frameElement.height-parseInt(moving_div.style.height),Math.max(0,event.clientY - parseInt(moving_div.style.height)/2))) + 'px')
          moving_div.style.top = String(Math.min(window.frameElement.height-parseInt(moving_div.style.height),Math.max(0,event.clientY - parseInt(moving_div.style.height)/2))) + 'px';
          moving_div.style.left = Math.min(window.frameElement.width-parseInt(moving_div.style.width),Math.max(0,event.clientX - parseInt(moving_div.style.width)/2)) + 'px';
          moving_div.style.borderStyle = "none"

          window.selected_div = " "
          // update output
          window.output[moving_div.id].push(
            {
              "time":getTime(),
              "x":moving_div.style.left,
              "y":moving_div.style.top,
              "overlap":this.id,
            }
          )
          
          // return updated value
          sendValue(window.output)
        }
      })
      /*
      // catch clicks outside of defined divs
      document.body.addEventListener("mouseup",function(){
        if (window.selected_div != " "){  
          var moving_div = document.getElementById(window.selected_div)
          moving_div.style.top = window.output[moving_div.id][0]["y"] //"0px"
          moving_div.style.left = window.output[moving_div.id][0]["x"]
        } 
      })
      */
      document.body.appendChild(goal)
      console.warn(key)
      console.warn(val_lst)
      
      g = g +1
    }
    sendValue(window.output)
    window.rendered = true
    Streamlit.setFrameHeight(parseFloat(window.screen.height)*comp_height)
    //Streamlit.setFrameHeight(window.screen.height*comp_height)
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(window.screen.height*.9)
