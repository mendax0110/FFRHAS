var count = 0;

function CountUp()
{
    count++;

    document.getElementById("count").innerText = count;
}

function FetchData()
{
    fetch("http://127.0.0.1:5000/get_data_from_backend")
        .then(Response => Response.text())
        .then(text => document.getElementById("data").innerText = text)
}