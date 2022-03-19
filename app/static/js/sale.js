document.getElementById('finished_date').min = new Date(new Date().getTime() + 60 * 60000).toISOString().split(".")[0].slice(0,-3)

// Modify the view when it is a dutch auction
function show(selected){
    if(selected == 'dutch'){
        document.getElementById('show').classList.remove('d-none')
        document.getElementById('final_bid').required = true
        $('label[for="initial_bid"]').text('Maximum price')
    }
    else{
        document.getElementById('show').classList.add('d-none')
        document.getElementById('final_bid').required = false
        $('label[for="initial_bid"]').text('Floor price')
    }
}

// Copy of the FileList that allows modifications
let dt = new DataTransfer()

// Calls the input
function loadUpload() { document.getElementById('upload').click() }

// Changes onclicks, hides and displays different elements
function settings() {
    document.getElementById('image').removeAttribute("onclick") // Delete input caller to the container
    document.getElementsByClassName('fa-plus')[0].setAttribute("onclick", "loadUpload()") // Add input caller to the add picture
    
    // Shows the delete picture
    document.getElementsByClassName('fa-trash')[0].classList.remove('d-none')
    
    // Calls directly to add element
    document.getElementById('upload').removeAttribute("onchange")
    document.getElementById('upload').setAttribute("onchange", "addFiles()")
    
    //Style things
    document.getElementsByClassName('fa-plus')[0].classList.remove('display-1')
    document.getElementsByClassName('fa-plus')[0].classList.add('h1')
    document.getElementById('image').classList.remove('d-flex')
    document.getElementById('image').classList.add('no-pointer')

    addFiles() // Create the carousel and add files
}

//TODO: No va cuando queda una imagen
function deleteImage() {
    dt.items.remove(document.getElementsByClassName('active')[0].getAttribute('data-bs-slide-to')) // Delete element active
    loadCarousel() // Reload carousel

    // Changes onclicks, hides and displays different elements
    if (dt.files.length == 0) {
        document.getElementsByClassName('fa-trash')[0].classList.add('d-none') // Hides the delete picture

        // Calls to settings again
        document.getElementById('upload').removeAttribute("onchange")
        document.getElementById('upload').setAttribute("onchange", "settings()")

        //Style things
        document.getElementsByClassName('fa-plus')[0].classList.add('display-1')
        document.getElementsByClassName('fa-plus')[0].classList.remove('h1')
        document.getElementById('image').classList.add('d-flex')
        document.getElementById('image').classList.remove('no-pointer')

        setTimeout(() => {
            document.getElementById('image').setAttribute("onclick", "loadUpload()") // Add input caller to the container
            document.getElementsByClassName('fa-plus')[0].removeAttribute("onclick") // Delete input caller to the add picture
        }, 100)
    }
}

function addFiles() {
    // Copy the fileList into the dataTransfer
    for (i = 0; i < document.getElementById('upload').files.length; i++) dt.items.add(document.getElementById('upload').files[i])

    // Delete repeated images
    for (i = dt.files.length - 1; i >= 1; i--) {
        for (j = i - 1; j >= 0; j--) {
            if (dt.files[i] != null && dt.files[i].lastModified == dt.files[j].lastModified && dt.files[i].size == dt.files[j].size && dt.files[i].name == dt.files[j].name && dt.files[i].type == dt.files[j].type) dt.items.remove(i)
        }
    }

    loadCarousel() // Reload carousel
}

// Creates carousel
function loadCarousel() {
    //Clear the images from the carousel
    while (document.getElementsByClassName('carousel-inner')[0].firstChild) document.getElementsByClassName('carousel-inner')[0].firstChild.remove()

    for (i = 0; i < dt.files.length; i++) {
        i == 0 ? (document.getElementsByClassName('carousel-indicators')[0].innerHTML = '<button type="button" data-bs-target="#carousel" data-bs-slide-to="' + i + '" class="active" aria-current="true" aria-label="Slide ' + (i + 1) + '"></button>') : (document.getElementsByClassName('carousel-indicators')[0].innerHTML += '<button type="button" data-bs-target="#carousel" data-bs-slide-to="' + i + '" aria-label="Slide ' + (i + 1) + '"></button>')
        i == 0 ? (document.getElementsByClassName('carousel-inner')[0].innerHTML = '<div class="carousel-item active"><img src="" class="d-block w-100"></div>') : (document.getElementsByClassName('carousel-inner')[0].innerHTML += '<div class="carousel-item"><img src="" class="d-block w-100"></div>')
        document.getElementsByClassName('carousel-item')[i].lastElementChild.src = URL.createObjectURL(dt.files[i])
    }

    // Show or hide controls depending quantity of images
    dt.files.length <= 1 ? document.getElementsByClassName('carousel-control-prev')[0].classList.add('d-none') : document.getElementsByClassName('carousel-control-prev')[0].classList.remove('d-none')
    dt.files.length <= 1 ? document.getElementsByClassName('carousel-control-next')[0].classList.add('d-none') : document.getElementsByClassName('carousel-control-next')[0].classList.remove('d-none')
    if (dt.files.length == 1) document.getElementsByClassName('carousel-indicators')[0].firstChild.remove()

    document.getElementById('upload').files = dt.files; // Add files into the input
}