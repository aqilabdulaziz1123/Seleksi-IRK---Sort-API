function changeAction(){
    // let algoritma = $("input[type='radio'][name='algoritma']:checked").val();
    let algoritma = document.querySelector('input[name="algoritma"]:checked').value;
    console.log(algoritma)
    document.getElementById("formdata").action =`/sort/${algoritma}`;
}