for(i= 0 ; i < document.getElementsByClassName('finished_date').length; i++){

    finished_date= new Date(document.getElementsByClassName('finished_date')[i].textContent).getTime()
    if(document.getElementsByClassName('created_date')[i] == undefined){
        countdown(finished_date, i, false)
        index= i
        setInterval(countdown, 1000 * 60, finished_date, index, false)
    }
    else{
        created_date = new Date(document.getElementsByClassName('created_date')[i].textContent).getTime()
        initial_bid = document.getElementsByClassName('initial_bid')[i].textContent
        final_bid = document.getElementsByClassName('final_bid')[i].textContent
        
        price_countdown(created_date, finished_date, initial_bid, final_bid, i, false)
        index= i
        setInterval(price_countdown, 1000 * 60, created_date, finished_date, initial_bid, final_bid, index, false)
    }
}