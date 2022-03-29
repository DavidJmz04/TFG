if(document.getElementById('winner') == undefined){
    finished_date = new Date(document.getElementsByClassName('finished_date')[0].textContent).getTime()
    
    if(document.getElementsByClassName('created_date')[0] == undefined){
        countdown(finished_date,0)
        
        setInterval(countdown, 1000, finished_date,0)
    }
    else{
        created_date = new Date(document.getElementsByClassName('created_date')[0].textContent).getTime()
        initial_bid = document.getElementsByClassName('initial_bid')[0].textContent
        final_bid = document.getElementsByClassName('final_bid')[0].textContent
    
        price_countdown(created_date, finished_date, initial_bid, final_bid, 0)
        
        setInterval(price_countdown, 1000, created_date, finished_date, initial_bid, final_bid, 0)
    }
}