import puppeteer from "puppeteer";
import fs from "fs";

const getBusinesses = async () => {
  const browser = await puppeteer.launch({
    headless: false, 
    defaultViewport: null
  })

  // open a new page
  const page = await browser.newPage();

  // on this new page
  await page.goto("https://www.businesslist.com.ng/state/ondo", {
    waitUntil: "domcontentloaded"
  })

  // get page data

 let businessArray = []; 
 var business;

  for (let index = 0; index < 38; index++) {
    business = await page.evaluate(() => {
  
        const busNameList= document.querySelectorAll(".company_header h4 a");
        const busNameListLength = busNameList.length;
  
        const busAddressList = document.querySelectorAll(".company_header .address");
        const busAddListLength = busAddressList.length;
  
        const busPhoneList = document.querySelectorAll(".company .cont .s .fa-phone + span");
        const busPhoneListLength = busPhoneList.length;
  
        const busNameArr = Array.from(busNameList).map(name => {
          const busName = name.innerText;
  
          return busName
        })
  
        const busAddArr = Array.from(busAddressList).map(address => {
          const busAdd = address.innerText;
  
          return busAdd
        })
  
        const busPhoneArr = Array.from(busPhoneList).map(phone => {
          const busPhone = phone.innerText;
  
          return busPhone
        })
  
        const busDetails = busNameArr.map((name, index) => {
          return {name, address:busAddArr[index], phoneNo:busPhoneArr[index] || null}
        })

        return busDetails;
      }
    )
    businessArray.push(business)
    if (index != 38){
      await page.click(".pages_container ul li a[rel=next]");
    }
  }
  
  const singleBusArr = businessArray.flat();
  // const jsonData = JSON.stringify(singleBusArr);
  await browser.close()
  return await singleBusArr
}

let jsonValue = await getBusinesses();

// convert json file to csv
function jsonToCsv(jsonVal) {
  let csv = '';
  
  // Extract headers
  const headers = Object.keys(jsonVal[0]);
  csv += headers.join(';') + '\n';
  
  // Extract values
  jsonVal.forEach(obj => {
      const values = headers.map(header => obj[header]);
      csv += values.join(';') + '\n';
  });
  
  return csv;
}

// Convert JSON to CSV
const csvData = jsonToCsv(jsonValue);

// write into file
fs.writeFile("ondoBusiness.csv", csvData, "utf-8", (err) => {
  if (err) console.log(err);
  else console.log("Data saved");
})