var elem = document.getElementById("table_rows_data");

let errors_str = elem.dataset.tabledata
console.log('======================================')
console.log(errors_str)
console.log(errors_str[0])

/*
let errors = [["bob", "depth", 1, .2, .3, .4, .5, .6],
["annie", "depth", .6, .8, .2, .9, 0.1, .7],
["bob", "height", 10, 20, 3, 40, 78, 9],
["annie", "height", 34, 5, 56, 23, 12, 12]]
;*/

/*
"[['Bob', 'Open', 0.2, 0.1, 0.2, 0.1, 0.1], 
['Joe', 'Open', 0.2, 0.1, 0.2, 0.1, 0.1]]""

*/

var errors = eval(errors_str);
console.log(errors)
console.log(errors[0])
  
  function produceTable(errorTable) {
    res = "";
    res += "<table>\n";
    for (error of errors) {
      res += "<tr>\n";
      res += "<td  class='user_button'>" + error[0] + "</td>\n";
      res += "<td  class='param_button'>" + error[1] + "</td>\n";
      res += "<td  class='MAE_button'>" + error[2] + "</td>\n";
      res += "<td  class='MAPE_button'>" + error[3] + "</td>\n";
      res += "<td  class='SMAPE_button'>" + error[4] + "</td>\n";
      res += "<td  class='MSE_button'>" + error[5] + "</td>\n";
      res += "<td  class='RMSE_button'>" + error[6] + "</td>\n";
      //res += "<td  class='r_button'>" + error[7] + "</td>\n";

      res += "</tr>\n";
    }
    res += "</table>\n";
    return res;
  }
  
  function sortBy(errorTable, col) {
    // console.log(col);
    errorTable.sort(function (a, b) {
      return a[col] < b[col] ? -1 : 1;
    });
  }
  // console.log(produceTable(cars));
  
  function sortTable(col) {
    sortBy(errors, col); // sorts "in place", i.e., modifies cars
    document.getElementById("theTable").innerHTML = produceTable(errors);
  }
  
  document.getElementById("theTable").innerHTML = produceTable(errors);
  