  
  function produceButtons() {
    b_res = "";
    b_res += "<table>"
    b_res += "<tr>"
    b_res += "<th class='user_button'>"
    b_res += "<button onclick='sortTable(0)'>USER</button>"
    b_res += "</th>"
    b_res += "<th class='param_button'>"
    b_res += "<button onclick='sortTable(1)'>Parameter</button>"
    b_res += "</th>"
    b_res += "<th class='MAE_button'>"
    b_res += "<button onclick='sortTable(2)'>MAE</button>"
    b_res += "</th>"
    b_res += "<th class='MAPE_button'>"
    b_res += "<button onclick='sortTable(3)'>MAPE</button>"
    b_res += "</th>"
    b_res += "<th class='SMAPE_button'>"
    b_res += "<button onclick='sortTable(4)'>SMAPE</button>"
    b_res += "</th>"
    b_res += "<th class='MSE_button'>"
    b_res += "<button onclick='sortTable(5)'>MSE</button>"
    b_res += "</th>"
    b_res += "<th class='RMSE_button'>"
    b_res += "<button onclick='sortTable(6)'>RMSE</button>"
    b_res += "</th>"
    b_res += "<th class='r_button'>"
    b_res += "<button onclick='sortTable(7)'>r-Value</button>"
    b_res += "</th>"
    b_res += "</tr>"
    b_res += "</table>"

    return b_res
  }


  function produceTable(errors) {
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
      res += "<td  class='r_button'>" + error[7] + "</td>\n";

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
  
  function create_buttons_and_table(buttons_id, table_id, data_id) {
    let elem = document.getElementById(data_id);
    let errors_str = elem.dataset.tabledata
    let errors = eval(errors_str);


    document.getElementById(buttons_id).innerHTML = produceButtons();
    document.getElementById(table_id).innerHTML = produceTable(errors);
  }