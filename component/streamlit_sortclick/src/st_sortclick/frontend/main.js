// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
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

    var output = {}
    console.warn(document.body.offsetWidth)
    const goal_width_base = document.body.offsetWidth/(Object.keys(values).length +1)
    console.warn(goal_width_base)
    const goal_height_base = screen.availHeight * .3
    window.selected_div = " "
    var g = 0
    for ( const [key, val_lst] of Object.entries(values)){
      // draw all files of category
      for ( i=0; i < val_lst.length; i++){
        // define used div
        var div = document.createElement("div")
        div.id = String(g)+"_"+String(i)

        // div location/visuals
        div.style.position = "absolute"
        div.innerHTML += String(val_lst[i])
        div.style.left = String(Math.round(Math.random() * document.body.offsetWidth))+"px"//String(Math.round(i * 100))+"px"
        div.style.top = "0px"
        div.style.width = "80px"
        div.style.height = "50px"
        //div.style.bottom= div.style.top + div.style.height
        div.style.cursor = "pointer"
        div.style.textAlign = "center"
        div.style.verticalAlign = "middle"
        div.style.backgroundColor = "grey"
        div.style.borderStyle = "solid"
        div.style.borderColor = "black"
        div.style.borderWidth = "3px"
        //div.style.backgroundColor = '#f1f1f1'
        div.addEventListener("mouseup", function(){
          if (window.selected_div!=" "){
            var last_selected = document.getElementById(window.selected_div)
            last_selected.style.borderColor = "black"
          } 
          this.style.borderColor = "red"
          window.selected_div = this.id
        })
        output[div.id] = Array(2)
        output[div.id][0] = div.style.left
        output[div.id][1] = false
        document.body.appendChild(div)
      }

      // add "folder" as goal structure
      var goal = document.createElement("div")
      goal.id = "goal_"+String(g)
      goal.innerHTML += "Bitte "+String(key)+" ablegen"//"stuff"//style.backroundColor="red"
      goal.style.width = String(parseInt(document.body.offsetWidth)*.2) + "px"//Math.floor(goal_width_base/100)*100+"px"//
      goal.style.height = window.screen.height * .2 +"px"
      goal.style.position = "absolute"
      goal.style.cursor = "pointer"
      goal.style.textAlign = "center"
      goal.style.verticalAlign = "middle"
      goal.style.zIndex = -10
      goal.style.bottom = "0px"
      goal.style.top = goal.style.bottom - goal.style.height
      goal.style.borderStyle = "solid"
      goal.style.borderColor = "black"
      goal.style.borderWidth = "3px"
      goal.style.left = String(((g+1)) * parseInt(goal_width_base) -parseInt(goal.style.width)/2)+"px"
      goal.style.backgroundColor = "grey"//cols[i]
      goal.addEventListener("mouseup", function(){
        if (window.selected_div != " "){
          var moving_div = document.getElementById(window.selected_div)
          console.warn(this.style.left)
          console.warn(window.selected_div)
          console.warn(moving_div.style.width)
          moving_div.style.top = String(parseInt(window.screen.height*.7)-(parseInt(this.style.height))+parseInt(moving_div.id.charAt(0)+1)*2 + 20) +"px"
          moving_div.style.left = String(parseInt(this.style.left) + parseInt(moving_div.id.split("_").pop()+ 1)*9)+"px"
          moving_div.style.borderColor = "black"
          window.selected_div = " "
          // update output
          output[moving_div.id][1] = this.id
          
          // return updated value
          sendValue(output)
        }
      })
      document.body.addEventListener("mouseup",function(){
        if (window.selected_div != " "){  
          var moving_div = document.getElementById(window.selected_div)
          moving_div.style.top = "0px"
          moving_div.style.left = output[moving_div.id][0]
          output[moving_div.id][1] = false
          sendValue(output)
        } 
      })
      document.body.appendChild(goal)
      console.warn(key)
      console.warn(val_lst)

      g = g +1
    }
/*
    for( i=0; i < values.length; i++){
      // define used div
      var div = document.createElement("div")
      div.id = "img_"+String(i)

      // div location/visuals
      div.style.position = "absolute"
      div.innerHTML += String(values[i])
      div.style.left = String(Math.round(Math.random() * document.body.offsetWidth))+"px"//String(Math.round(i * 100))+"px"
      div.style.top = "0px"
      
      div.style.height = "50px"
      //div.style.bottom= div.style.top + div.style.height
      div.style.cursor = "pointer"
      div.style.textAlign = "center"
      div.style.verticalAlign = "middle"
      div.style.backgroundColor = "grey"
      div.style.borderStyle = "solid"
      div.style.borderColor = "black"
      div.style.borderWidth = "3px"
      //div.style.backgroundColor = '#f1f1f1'
      div.addEventListener("mouseup", function(){
        if (window.selected_div!=" "){
          var last_selected = document.getElementById(window.selected_div)
          last_selected.style.borderColor = "black"
        } 
        this.style.borderColor = "red"
        window.selected_div = this.id
      })

      // make goals
      var goal = document.createElement("div")
      goal.id = "goal_"+String(i)
      goal.innerHTML += "Bitte "+String(values[i])+" ablegen"//"stuff"//style.backroundColor="red"
      goal.style.width = String(parseInt(document.body.offsetWidth)*.1) + "px"//Math.floor(goal_width_base/100)*100+"px"//
      goal.style.height = window.screen.height * .1 +"px"
      goal.style.position = "absolute"
      goal.style.cursor = "pointer"
      goal.style.textAlign = "center"
      goal.style.verticalAlign = "middle"
      goal.style.zIndex = -10
      goal.style.bottom = "0px"
      goal.style.top = goal.style.bottom - goal.style.height
      goal.style.borderStyle = "solid"
      goal.style.borderColor = "black"
      goal.style.borderWidth = "3px"
      goal.style.left = String(((i+1)) * parseInt(goal_width_base) -parseInt(goal.style.width)/2)+"px"
      goal.style.backgroundColor = "grey"//cols[i]
      goal.addEventListener("mouseup", function(){
        if (window.selected_div != " "){
          var moving_div = document.getElementById(window.selected_div)
          console.warn(window.screen.height*.7)
          moving_div.style.top = String(parseInt(window.screen.height*.7)-(parseInt(this.style.height)+ parseInt(moving_div.style.height))/2) +"px"
          moving_div.style.left = String(parseInt(this.style.left) + (parseInt(this.style.width) - parseInt(moving_div.style.width))/2)+"px"
          moving_div.style.borderColor = "black"
          window.selected_div = " "
          // update output
          output[moving_div.id][1] = this.id
          
          // return updated value
          sendValue(output)
        }
      })
      document.body.addEventListener("mouseup",function(){
        if (window.selected_div != " "){  
          var moving_div = document.getElementById(window.selected_div)
          moving_div.style.top = "0px"
          moving_div.style.left = output[moving_div.id][0]
          output[moving_div.id][1] = false
          sendValue(output)
        } 
      })
      output[div.id] = Array(2)
      output[div.id][0] = div.style.left
      output[div.id][1] = false
      //div.style.width = String(parseInt(goal.style.width)*.4) + "px"
    }
    */
    // You'll most likely want to pass some data back to Python like this
    // sendValue({output1: "foo", output2: "bar"})
    // sendValue("test")
    window.rendered = true
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(window.screen.height*.7)
