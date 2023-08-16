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
    const {img, key} = event.detail.args
    for( i=0; img.length; i++){
      document.body.clientHeight = "500px"
      
      var div = document.getElementById("img_"+i)
      //div.style
      div.style.left = String(i * 100)+"px"
      const cols = ["red","blue","yellow"]
      
      // make goals
      var goal = document.createElement("div")
      goal.innerHTML += "stuff"//style.backroundColor="red"
      goal.style.width = "100px"
      goal.style.height = "200px"
      goal.style.position = "absolute"
      goal.style.textAlign = "center"
      goal.style.verticalAlign = "middle"
      goal.style.zIndex = -10
      goal.style.top = "50px"
      goal.style.left = String(i * 100)+"px"
      goal.style.borderColor ="black"
      goal.style.borderWidth = "5px"
      goal.style.backgroundColor = cols[i]
      
      //goal.value="goal_"+String(i)
      
      document.body.appendChild(goal)
      //div.style.top = String(Math.floor(Math.random() * (600-300))+300)+"px"
    }
    window.rendered = true
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(100)
