var websocket;
var ros;
var pub_text;
var sub_text;
var sub_img;

function log(who, str) {
    $("#output").val(who+str + "\n" + $("#output").val());
}

function pub_msg(text) {
    var msg = new ROSLIB.Message({
        data: text
    });
    pub_text.publish(msg);
}

function setup_ros() {
    ros = new ROSLIB.Ros({
        url: websocket
    });

    ros.on('connection', () => {
        log("System: ",'Connection with the robot established.');
    });

    ros.on('error', (error) => {
        log("System: ",'Connection error with the robot.', error);
        // close_connection();
    });

    ros.on('close', () => {
        log("System: ",'Connection with the robot has been closed.');
        // close_connection();
    });

    pub_text = new ROSLIB.Topic({
        ros: ros,
        name: '/action_tesp',
        messageType: 'std_msgs/String'
    });

    sub_text = new ROSLIB.Topic({
        ros: ros,
        name: '/logger_web',
        messageType: 'std_msgs/String'
    });

    sub_img = new ROSLIB.Topic({
        ros : ros,
        name : '/camera/rgb/image_raw_3',
        messageType : 'sensor_msgs/CompressedImage'
    });

    sub_text.subscribe(function (text) {
        log("Robot: ", text.data);
    });
    
    // Define a callback function to handle the incoming image data
    sub_img.subscribe(function(msg) {
        var img = new Image();
        img.src = "data:image/jpeg;base64," + msg.data;
        // When the image is loaded, draw it on a canvas element
        img.onload = function() {
            // Create a canvas element and set its dimensions to match the image
            var canvas = document.getElementById('canvas_img');    
            // Get the 2D context of the canvas and draw the image on it
            var ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
        }
    });
    
}

$(document).ready(() => {
    ip = "127.0.0.1" // or location.hostname
    websocket = "ws://" + ip + ":9090"; //to have a url
    setup_ros(); //connect to ros

    $("#actions").on('click', (event) => {
        console.log(event.target);
        var obj = $(event.target).attr("id");
        log("User: ",obj);
        pub_msg(obj);
    });

    document.addEventListener("keypress", (e) => {
        var obj;
        if (e.key === "w" || e.key === "W" || e.key == "ArrowUp")
        {
            obj = "up";
            log("User: ",obj);
            pub_msg(obj);
        }
        else if (e.key === "s" || e.key === "S" || e.key === "ArrowDown")
        {
            obj = "down";
            log("User: ",obj);
            pub_msg(obj);
        }
        else if(e.key === "d" || e.key === "D" || e.key === "ArrowRight")
        {
            obj = "right";
            log("User: ",obj);
            pub_msg(obj);
        }
        else if(e.key === "a" || e.key === "A" || e.key === "ArrowLeft")
        {
            obj = "left";
            log("User: ",obj);
            pub_msg(obj);
        }
    })

    $("#input_text").keypress(function(event) {
        var key = (event.keyCode ? event.keyCode : event.which);
        if (key === 13 || key === 'Enter') {
            event.preventDefault();
            msg = $("#input_text").val();
            $("#input_text").val('');
            log("User",msg);
            pub_msg(msg);
        }
     });
});