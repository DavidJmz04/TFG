/* Creates countdown */
function countdown(finished_date, index, products= true){
    now = new Date().getTime()
    diff= finished_date - now  
    
    if(diff > 0) {
        days = Math.floor(finished_date / 86400000 - now / 86400000)
        hours = products ? ('0' + Math.floor((finished_date / 3600000 - now / 3600000) % 24)).slice(-2) : Math.floor((finished_date / 3600000 - now / 3600000) % 24)
        minutes = products ? ('0' + Math.floor((finished_date / 60000 - now / 60000) % 60)).slice(-2) : Math.floor((finished_date / 60000 - now / 60000) % 60)

        document.getElementsByClassName('countdown')[index].innerHTML = ((days != 0) ? days + ' days ' : '') + (!products ? hours + ' hours ' + minutes + ' minutes' : hours + ':' + minutes + ':' + ('0' + Math.floor((finished_date / 1000 - now / 1000) % 60)).slice(-2))
    }
    else document.getElementsByClassName('countdown')[index].innerHTML = 'Finished'
}

/* Creates a price countdown depending the remaining time */
function price_countdown(created_date, finished_date, initial_bid, final_bid, index, products= true){
    now = new Date().getTime()
    diff= finished_date - now
    
    if(diff > 0) document.getElementsByClassName('countdown')[index].innerHTML = (!products ? 'Current bid: ' : '') + (initial_bid - (((initial_bid - final_bid) * (100 - ((diff * 100) / (finished_date - created_date)))) / 100).toFixed(2)) + '€'
    else document.getElementsByClassName('countdown')[index].innerHTML = 'Finished'
}