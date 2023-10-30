// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

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

function goalCollition(data, data_goals){
  if (data["b"] < data_goals[0]["top"]){
    return false
  }else{
    console.error(data["b"])
    console.error(data_goals)
    for (j = 0; j<Object.keys(data_goals).length;j++){
      goal = data_goals[j]
      if ((data["l"]<=goal["r"]) & (data["l"]>=goal["l"]) ||(data["r"]<=goal["r"]) & (data["r"]>=goal["l"])){
        return goal["id"]
      }
    }
    return false
  }
}
function disableSelect(event) {
  event.preventDefault();
}
function onmouseDown(el){
  if (window.selected_div == " " ){
    window.addEventListener('mousemove',x=  function(event){ moveDiv(el, event)})
    window.addEventListener('mouseup', y = function(event){ onMouseUp(el,event)})
    window.addEventListener('selectstart', disableSelect);
    window.selected_div == el.id
    el.style.zIndex = 10
  }
}
function moveDiv(el,event){
  console.warn(window.frameElement.height)
  console.warn(event.clientY)
  el.style.top = Math.min(window.frameElement.height-parseInt(el.style.height),Math.max(0,event.clientY - parseInt(el.style.height)/2)) + 'px';
  el.style.left = Math.min(window.frameElement.width-parseInt(el.style.width),Math.max(0,event.clientX - parseInt(el.style.width)/2)) + 'px';
  
}
function onMouseUp(el){
  console.warn ("triggered")
  window.removeEventListener('mousemove', x)
  window.removeEventListener('mouseup', y)
  window.removeEventListener('selectstart', disableSelect);
  window.selected_div == " "
  el.style.zIndex = 0
  console.log(el.style.top)
  console.log(el.style.height)
  console.log(window.coll)
  overlap = goalCollition(
    {
      "b":parseInt(el.style.top) + parseInt(el.style.height), 
      "l":parseInt(el.style.left),
      "r":parseInt(el.style.left)+parseInt(el.style.width)
    }
    ,window.coll
  )
  console.log(overlap)
  console.warn(typeof(window.output[el.id]))
  // write to output
  window.output[el.id].push(
    {
      "time":getTime(),
      "x" : parseInt(window.scrollX)+parseInt(el.style.left), 
      "y": parseInt(window.scrollY)+parseInt(el.style.top), 
      "overlap": overlap
    }
  )
  // return output
  sendValue(window.output)
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
    //const {img, key} = event.detail.args
    const {values, comp_height, key} = event.detail.args
    window.output = {}
    window.coll = {}
    const goal_width_base = document.body.offsetWidth/(Object.keys(values).length +1)
    window.selected_div = " "
    //const goal_width_base = screen.availWidth/(values.length +1)
    //const goal_height_base = screen.availHeight * .6
    // save data wherer div is located --> dont use for mouse travel way --> use mouse events
    var g = 0
    for (const [key, val_lst] of Object.entries(values)){
      for( i = 0; i < val_lst.length; i++){
        // generate movable div
        var div = document.createElement('div')
        div.id = String(g)+'_'+String(i)
        div.classList.add("datei_container")

        // define starting location
        div.style.left = String(Math.round(Math.random() * document.body.offsetWidth*.95))+"px"
        div.style.top = String(Math.round(Math.random() * window.frames.innerHeight*.3))+"px"
        div.style.width = "50px"
        div.style.height = "50px"
        
        img = document.createElement('img')
        img.src = "./Datei.png"
        img.classList.add("datei_img")
        
        file_name = document.createElement('div')
        file_name.classList.add("datei_name")
        file_name.innerHTML += String(val_lst[i])
        
        div.appendChild(img)
        div.appendChild(file_name)
        

        // added movability
        div.addEventListener('mousedown', function(){onmouseDown(this)})
        // init output 
        window.output[div.id] = [
          {
            "time":getTime(),
            "x" : parseInt(div.style.left) + (parseInt(div.style.width)/2), 
            "y": parseInt(div.style.top)+parseInt(div.style.height)/2, 
            "overlap":false
          }]
        // add to doc
        document.body.appendChild(div)
      }
      console.warn(window.output)

      // generate goal structure
      var goal = document.createElement("div")
      goal.id = "goal_"+String(g)
      goal.innerHTML += "Bitte "+String(key)+" ablegen"//"stuff"//style.backroundColor="red"
      goal.classList.add("goal")
      goal.style.width = String(parseInt(document.body.offsetWidth)*.2) + "px"//Math.floor(goal_width_base/100)*100+"px"//
      goal.style.bottom = "0px"
      goal.style.height = window.screen.height * .2 +"px"
      goal.style.left = String(((g+1)) * parseInt(goal_width_base) -parseInt(goal.style.width)/2)+"px"
      
      window.coll[g] = {
        "top" : parseInt(window.frames.innerHeight) - parseInt(goal.style.height), 
        "l":parseInt(goal.style.left), 
        "r":parseInt(goal.style.left)+parseInt(goal.style.width), 
        "id": goal.id
      }

      // add goals to doc
      document.body.appendChild(goal)
      g++
     
    }
    sendValue(window.output)
    console.warn(window.output)
    console.info(window.screen.height)
    console.info(comp_height)
    Streamlit.setFrameHeight(parseFloat(window.screen.height)*comp_height)
    window.rendered = true
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
Streamlit.setFrameHeight(window.screen.height*.7)