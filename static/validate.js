function capitalize(s)
{   
    let str = s.trim()
    let ret = str[0].toUpperCase() + str.slice(1).toLowerCase();
    return ret;
}

function checkNumber(input, input_name, min_len, max_len) {
    if (input % 1 != 0) {
        Swal.fire('Wartość w polu <b>'+input_name+'</b> musi być liczbą całkowitą', '' , 'info');
        return false;
    } else if (input > max_len || input < min_len) {
        Swal.fire('Wartość w polu <b>'+input_name+'</b> musi należeć do przedziału od '+min_len+' do '+max_len, '' , 'info');
        return false;
    } else {
        return true;
    }  
}

function checkFloatNumber(input, input_name, min_len, max_len) {
    if (input > max_len || input < min_len) {
        Swal.fire('Wartość w polu <b>'+input_name+'</b> musi należeć do przedziału od '+min_len+' do '+max_len, '' , 'info');
        return false;
    } else {
        return true;
    }  
}