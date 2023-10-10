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
    const {values, key} = event.detail.args
    window.output = {}
    console.warn(document.body.offsetWidth)
    const goal_width_base = document.body.offsetWidth/(Object.keys(values).length +1)
    console.warn(goal_width_base)
    window.selected_div = " "
    var g = 0
    for ( const [key, val_lst] of Object.entries(values)){
      // draw all files of category
      for ( i=0; i < val_lst.length; i++){
        // define used div
        var div = document.createElement("div")
        div.id = String(g)+"_"+String(i)
        div.classList.add('datei')
        div.innerHTML += String(val_lst[i])
        div.style.left = String(Math.round(Math.random() * (document.body.offsetWidth*.95)))+"px"//String(Math.round(i * 100))+"px"
        div.style.top = String(Math.round(Math.random() *  window.frames.innerHeight*.3))+"px"//"0px"
        div.addEventListener("mouseup", function(){
          if (window.selected_div!=" "){
            var last_selected = document.getElementById(window.selected_div)
            last_selected.style.borderColor = "black"
          } 
          this.style.borderColor = "red"
          window.selected_div = this.id
        })

        window.output[div.id] = [
          {
            "time":getTime(),
            "x":div.style.left,
            "y":div.style.top,
            "overlap":false
          }]
        document.body.appendChild(div)
      }

      // add "folder" as goal structure
      var goal = document.createElement("div")
      goal.id = "goal_"+String(g)
      goal.classList.add('goal')
      goal.innerHTML += "Bitte "+String(key)+" ablegen"//"stuff"//style.backroundColor="red"
      goal.style.width = String(parseInt(document.body.offsetWidth)*.2) + "px"//Math.floor(goal_width_base/100)*100+"px"//
      goal.style.height = window.screen.height * .2 +"px"
      goal.style.top = goal.style.bottom - goal.style.height
      goal.style.left = String(((g+1)) * parseInt(goal_width_base) -parseInt(goal.style.width)/2)+"px"
      goal.addEventListener("mouseup", function(){
        if (window.selected_div != " "){
          var moving_div = document.getElementById(window.selected_div)
          console.warn(this.style.left)
          console.warn(window.selected_div)
          console.warn(moving_div.style.width)
          moving_div.style.top = String(parseInt(window.screen.height*.7)-(parseInt(this.style.height))+parseInt(moving_div.id.charAt(0)+1)*2 + 20) +"px"
          moving_div.style.left = String(parseInt(this.style.left) + parseInt(moving_div.id.split("_").pop()+ 1)*9)+"px"//String(parseInt(this.style.left) + Math.floor(Math.random() * (parseInt(this.style.width)*.8  + 1)))+"px"
          //Math.floor(Math.random() * (parseInt(this.style.width)*.8  + 1))
          moving_div.style.borderColor = "black"
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
      document.body.addEventListener("mouseup",function(){
        if (window.selected_div != " "){  
          var moving_div = document.getElementById(window.selected_div)
          moving_div.style.top = window.output[moving_div.id][0]["y"] //"0px"
          moving_div.style.left = window.output[moving_div.id][0]["x"]
        } 
      })
      document.body.appendChild(goal)
      console.warn(key)
      console.warn(val_lst)
      
      g = g +1
    }
    sendValue(window.output)
    window.rendered = true
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(window.screen.height*.7)
