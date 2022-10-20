
//Images
var imageCycleTime = 10000 //in ms
var calendarCycleTime = 11000 //in ms

function Startup(){
    GetImages();
    GetCalendar();
}

//Cycle Through Images
var i=0;
var imageList = [];
let checkInterval;

function ChangeImage(){
    GetImages(); //checks for new images and ads all images to the DOM
    var images = document.getElementsByClassName("image")
    images[i].style.display ="none";
    if (i<images.length-1) {
        i++;
    } else {
        i=0;
    }
    //console.log(i);
    images[i].style.display ="block";
}

function GetImages() {
    $.ajax({
        type: "POST",
        data: {to_send: " "},
        url: "/cgi-bin/GetImages.py",
        success: PostImages
        });
}

function PostImages(response) {
    //console.log('PostImages Ran');
    //console.log(response);
    //console.log(JSON.stringify(imageList) != JSON.stringify(response));
    if (JSON.stringify(imageList) != JSON.stringify(response)) {
        imageList = response;
        console.log("New Files");
        console.log(imageList);
        var images = []
        var count = 1
        document.getElementById("images").innerHTML = '';
        for (const img in response) {
            var newImage = document.createElement('img');
            newImage.src = 'img\\' + response[img];
            newImage.id = 'img' + count;
            newImage.classList.add("image");
            document.getElementById("images").appendChild(newImage);
            count += 1;
            
        }
        ChangeImage();
        if (!checkInterval) {
            checkInterval = setInterval(ChangeImage, imageCycleTime);
        }
    }
}
















//Calendar


function GetCalendar(){
    //console.log("GetCalendar ran");
    $.ajax({
    type: "POST",
    data: {to_send: "verifyCalendar"},
    url: "/cgi-bin/GetCalendar.py",
    success: UpdateCalendar
    });
}

let calendarInterval;
if (!calendarInterval) {
    calendarInterval = setInterval(GetCalendar, calendarCycleTime);
}

var calendarInfo = []
function UpdateCalendar(response){
    //console.log('Return_Data Ran');
    if (JSON.stringify(calendarInfo) != JSON.stringify(response)) {
        calendarInfo = response;
        //console.log(response);
        populateCalendar(response);
    }

}

function populateCalendar(calendar) {
    //Loop to make days
    console.log(calendar);
    document.getElementById('calendar').innerHTML = ""
    for (const day in calendar['projects']) {
        var newDay = document.createElement('div');
        newDay.classList.add('calendarDay');
        var newDate = document.createElement('div');
        newDate.classList.add('calendarDate');
        newDate.innerHTML = day;

        newDay.append(newDate);



        //if day has day off add it


        //Add installer and job divs
        //console.log(calendar['projects'][day]);
        var jobs = calendar['projects'][day]
        for (const job in jobs) {
            console.log(jobs[job]);


            var container = document.createElement('div');
            container.classList.add('calendarJobContainer');


            var installer = document.createElement('div');
            installer.classList.add('calendarInstaller');
            installer.innerHTML = jobs[job]['installer'];

            var jobName = document.createElement('div');
            jobName.classList.add('calendarJob');
            jobName.innerHTML = jobs[job]['jobs'];

            container.append(installer);
            container.append(jobName);

            newDay.append(container);

        }


        document.getElementById('calendar').append(newDay);
    }
    
        //Add time off

}


Startup();