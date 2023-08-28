// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function goalCollition(data, data_goals){
  if (data["b"] < data_goals[0]["top"]){
    return false
  }else{
    for (j = 0; j<Object.keys(data_goals).length;j++){
      goal = data_goals[j]
      if ((data["l"]<=goal["r"]) & (data["l"]>=goal["l"]) ||(data["r"]<=goal["r"]) & (data["r"]>=goal["l"])){
        return goal["id"]
      }
    }
    return false
  }
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  if (!window.rendered ) {
    // You most likely want to get the data passed in like this
    // const {input1, input2, input3} = event.detail.args
    const {img, key} = event.detail.args
    var output = {}
    var coll = {}
    const goal_width_base = screen.availWidth/(img.length +1)
    const goal_height_base = screen.availHeight * .6
    // save data wherer div is located --> dont use for mouse travel way --> use mouse events

    //const h = body.screen.height
    for( i=0; i < img.length; i++){
      document.body.clientHeight = "500px"
      var div = document.getElementById("img_"+String(i))
      //div.style
      div.style.left = String(Math.round(Math.random() * screen.availWidth*.8 +screen.availWidth*.1))+"px"
      div.style.top = "0px"
      div.style.width = "30px"//"100px"
      div.style.height = "50px"
      
      const cols = ["red","blue","yellow"]
      
      // make goals
      var goal = document.createElement("div")
      goal.id = "goal_"+String(i)
      goal.innerHTML += "Bitte "+String(img[i])+" ablegen"//"stuff"//style.backroundColor="red"
      goal.style.width = Math.floor(goal_width_base/100)*100+"px"//"100px"
      goal.style.height = "200px"
      goal.style.position = "absolute"
      goal.style.textAlign = "center"
      goal.style.verticalAlign = "middle"
      goal.style.zIndex = -10
      goal.style.top = goal_height_base+"px"
      goal.style.borderStyle = "solid"
      goal.style.borderColor = "black"
      goal.style.borderWidth = "3px"
      goal.style.left = String((i+.5) * goal_width_base)+"px"
      goal.style.backgroundColor = "grey"//cols[i]
      coll[i] = {"top" : parseInt(goal.style.top), "l":parseInt(goal.style.left), "r":parseInt(goal.style.left)+parseInt(goal.style.width), "id": goal.id}
      
      //goal.value="goal_"+String(i)
      output[div.id] = [{"x" : parseInt(window.scrollX)+parseInt(div.style.left), "y": parseInt(window.scrollY)+parseInt(div.style.top), "overlap":false}]
      console.warn(parseInt(div.style.left)+parseInt(div.style.width))
      div.addEventListener("mouseup", function(e){output[e.target.id].push({"x" : parseInt(window.scrollX)+parseInt(e.target.style.left), "y": parseInt(window.scrollY)+parseInt(e.target.style.top), "overlap":goalCollition({"b":parseInt(e.target.style.top) + parseInt(e.target.style.height), "l":parseInt(e.target.style.left),"r":parseInt(e.target.style.left)+parseInt(e.target.style.width)},coll)})})// saveData("sutkajsdhfl")) //send new pos of div
      document.addEventListener("pointerleave", function(e){ sendValue(output)}) //return val to python
      document.body.appendChild(goal)
    }
    console.warn(output)
    window.rendered = true
    
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
Streamlit.setFrameHeight(window.screen.height*.7)