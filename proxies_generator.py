from scrawl import *
import time


c = Crawl()

# project_path = rf'/var/www/html/api/client_process/scripts'
# project_path = rf'D:\job_scraping\job_script\logs'

# Date and time
start_time = time.time()
current_time = datetime.now().strftime("%H-%M-%S")
created_on = date.today().strftime("%Y-%m-%d")

# Create and configure logger 
# automation_logs = '/var/www/html/core_data/logs/proxies_logs'
automation_logs = f'{project_path}/proxies_logs'

if not os.path.exists(automation_logs): os.mkdir(automation_logs)

generate_report_logs = f'{automation_logs}/generate_report_logs'
if not os.path.exists(generate_report_logs): os.mkdir(generate_report_logs)

logging.basicConfig(filename=f"{generate_report_logs}/{created_on}_{current_time}.log", 
                    format='%(asctime)s %(process)d %(message)s', filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.INFO) 

start_time = time.time()

logger.info("Process Started ...\n")
proxy_col = dashboard['proxies']

# clear collection
proxy_col.drop()
logger.info("Proxies collection dropped \n")

url = 'http://list.didsoft.com/get?email=valleynest@gmail.com&pass=sxzktp&pid=http1000&showcountry=yes&level=1'

r = requests.get(url)
proxies = r.text


country_dic = { "AF" : "Afghanistan",
                "AX" : "Aland Islands",
                "AL" : "Albania",
                "DZ" : "Algeria",
                "AS" : "American Samoa",
                "AD" : "Andorra",
                "AO" : "Angola",
                "AI" : "Anguilla",
                "AQ" : "Antarctica",
                "AG" : "Antigua and Barbuda",
                "AR" : "Argentina",
                "AM" : "Armenia",
                "AW" : "Aruba",
                "AU" : "Australia",
                "AT" : "Austria",
                "AZ" : "Azerbaijan",
                "BS" : "Bahamas",
                "BH" : "Bahrain",
                "BD" : "Bangladesh",
                "BB" : "Barbados",
                "BY" : "Belarus",
                "BE" : "Belgium",
                "BZ" : "Belize",
                "BJ" : "Benin",
                "BM" : "Bermuda",
                "BT" : "Bhutan",
                "BO" : "Bolivia",
                "BQ" : "Bonaire, Saint Eustatius and Saba ",
                "BA" : "Bosnia and Herzegovina",
                "BW" : "Botswana",
                "BV" : "Bouvet Island",
                "BR" : "Brazil",
                "IO" : "British Indian Ocean Territory",
                "VG" : "British Virgin Islands",
                "BN" : "Brunei",
                "BG" : "Bulgaria",
                "BF" : "Burkina Faso",
                "BI" : "Burundi",
                "KH" : "Cambodia",
                "CM" : "Cameroon",
                "CA" : "Canada",
                "CV" : "Cape Verde",
                "KY" : "Cayman Islands",
                "CF" : "Central African Republic",
                "TD" : "Chad",
                "CL" : "Chile",
                "CN" : "China",
                "CX" : "Christmas Island",
                "CC" : "Cocos Islands",
                "CO" : "Colombia",
                "KM" : "Comoros",
                "CK" : "Cook Islands",
                "CR" : "Costa Rica",
                "HR" : "Croatia",
                "CU" : "Cuba",
                "CW" : "Curacao",
                "CY" : "Cyprus",
                "CZ" : "Czech Republic",
                "CD" : "Democratic Republic of the Congo",
                "DK" : "Denmark",
                "DJ" : "Djibouti",
                "DM" : "Dominica",
                "DO" : "Dominican Republic",
                "TL" : "East Timor",
                "EC" : "Ecuador",
                "EG" : "Egypt",
                "SV" : "El Salvador",
                "GQ" : "Equatorial Guinea",
                "ER" : "Eritrea",
                "EE" : "Estonia",
                "ET" : "Ethiopia",
                "FK" : "Falkland Islands",
                "FO" : "Faroe Islands",
                "FJ" : "Fiji",
                "FI" : "Finland",
                "FR" : "France",
                "GF" : "French Guiana",
                "PF" : "French Polynesia",
                "TF" : "French Southern Territories",
                "GA" : "Gabon",
                "GM" : "Gambia",
                "GE" : "Georgia",
                "DE" : "Germany",
                "GH" : "Ghana",
                "GI" : "Gibraltar",
                "GR" : "Greece",
                "GL" : "Greenland",
                "GD" : "Grenada",
                "GP" : "Guadeloupe",
                "GU" : "Guam",
                "GT" : "Guatemala",
                "GG" : "Guernsey",
                "GN" : "Guinea",
                "GW" : "Guinea-Bissau",
                "GY" : "Guyana",
                "HT" : "Haiti",
                "HM" : "Heard Island and McDonald Islands",
                "HN" : "Honduras",
                "HK" : "Hong Kong",
                "HU" : "Hungary",
                "IS" : "Iceland",
                "IN" : "India",
                "ID" : "Indonesia",
                "IR" : "Iran",
                "IQ" : "Iraq",
                "IE" : "Ireland",
                "IM" : "Isle of Man",
                "IL" : "Israel",
                "IT" : "Italy",
                "CI" : "Ivory Coast",
                "JM" : "Jamaica",
                "JP" : "Japan",
                "JE" : "Jersey",
                "JO" : "Jordan",
                "KZ" : "Kazakhstan",
                "KE" : "Kenya",
                "KI" : "Kiribati",
                "XK" : "Kosovo",
                "KW" : "Kuwait",
                "KG" : "Kyrgyzstan",
                "LA" : "Laos",
                "LV" : "Latvia",
                "LB" : "Lebanon",
                "LS" : "Lesotho",
                "LR" : "Liberia",
                "LY" : "Libya",
                "LI" : "Liechtenstein",
                "LT" : "Lithuania",
                "LU" : "Luxembourg",
                "MO" : "Macao",
                "MK" : "Macedonia",
                "MG" : "Madagascar",
                "MW" : "Malawi",
                "MY" : "Malaysia",
                "MV" : "Maldives",
                "ML" : "Mali",
                "MT" : "Malta",
                "MH" : "Marshall Islands",
                "MQ" : "Martinique",
                "MR" : "Mauritania",
                "MU" : "Mauritius",
                "YT" : "Mayotte",
                "MX" : "Mexico",
                "FM" : "Micronesia",
                "MD" : "Moldova",
                "MC" : "Monaco",
                "MN" : "Mongolia",
                "ME" : "Montenegro",
                "MS" : "Montserrat",
                "MA" : "Morocco",
                "MZ" : "Mozambique",
                "MM" : "Myanmar",
                "NA" : "Namibia",
                "NR" : "Nauru",
                "NP" : "Nepal",
                "NL" : "Netherlands",
                "AN" : "Netherlands Antilles",
                "NC" : "New Caledonia",
                "NZ" : "New Zealand",
                "NI" : "Nicaragua",
                "NE" : "Niger",
                "NG" : "Nigeria",
                "NU" : "Niue",
                "NF" : "Norfolk Island",
                "KP" : "North Korea",
                "MP" : "Northern Mariana Islands",
                "NO" : "Norway",
                "OM" : "Oman",
                "PK" : "Pakistan",
                "PW" : "Palau",
                "PS" : "Palestinian Territory",
                "PA" : "Panama",
                "PG" : "Papua New Guinea",
                "PY" : "Paraguay",
                "PE" : "Peru",
                "PH" : "Philippines",
                "PN" : "Pitcairn",
                "PL" : "Poland",
                "PT" : "Portugal",
                "PR" : "Puerto Rico",
                "QA" : "Qatar",
                "CG" : "Republic of the Congo",
                "RE" : "Reunion",
                "RO" : "Romania",
                "RU" : "Russia",
                "RW" : "Rwanda",
                "BL" : "Saint Barthelemy",
                "SH" : "Saint Helena",
                "KN" : "Saint Kitts and Nevis",
                "LC" : "Saint Lucia",
                "MF" : "Saint Martin",
                "PM" : "Saint Pierre and Miquelon",
                "VC" : "Saint Vincent and the Grenadines",
                "WS" : "Samoa",
                "SM" : "San Marino",
                "ST" : "Sao Tome and Principe",
                "SA" : "Saudi Arabia",
                "SN" : "Senegal",
                "RS" : "Serbia",
                "CS" : "Serbia and Montenegro",
                "SC" : "Seychelles",
                "SL" : "Sierra Leone",
                "SG" : "Singapore",
                "SX" : "Sint Maarten",
                "SK" : "Slovakia",
                "SI" : "Slovenia",
                "SB" : "Solomon Islands",
                "SO" : "Somalia",
                "ZA" : "South Africa",
                "GS" : "South Georgia and the South Sandwich Islands",
                "KR" : "South Korea",
                "SS" : "South Sudan",
                "ES" : "Spain",
                "LK" : "Sri Lanka",
                "SD" : "Sudan",
                "SR" : "Suriname",
                "SJ" : "Svalbard and Jan Mayen",
                "SZ" : "Swaziland",
                "SE" : "Sweden",
                "CH" : "Switzerland",
                "SY" : "Syria",
                "TW" : "Taiwan",
                "TJ" : "Tajikistan",
                "TZ" : "Tanzania",
                "TH" : "Thailand",
                "TG" : "Togo",
                "TK" : "Tokelau",
                "TO" : "Tonga",
                "TT" : "Trinidad and Tobago",
                "TN" : "Tunisia",
                "TR" : "Turkey",
                "TM" : "Turkmenistan",
                "TC" : "Turks and Caicos Islands",
                "TV" : "Tuvalu",
                "VI" : "U.S. Virgin Islands",
                "UG" : "Uganda",
                "UA" : "Ukraine",
                "AE" : "United Arab Emirates",
                "GB" : "United Kingdom",
                "US" : "United States",
                "UM" : "United States Minor Outlying Islands",
                "UY" : "Uruguay",
                "UZ" : "Uzbekistan",
                "VU" : "Vanuatu",
                "VA" : "Vatican",
                "VE" : "Venezuela",
                "VN" : "Vietnam",
                "WF" : "Wallis and Futuna",
                "EH" : "Western Sahara",
                "YE" : "Yemen",
                "ZM" : "Zambia",
                "ZW" : "Zimbabwe"
 }


number_of_ip = 0
number_of_country = set()

list_proxies = []
for x in proxies.split():
    x = x.split('#')

    if x[1]=='':
        continue
    list_proxies.append({
                    "country_code" : x[1],
                    "ip"           : x[0],
                    "country" : country_dic[x[1]]
                    })
    number_of_ip += 1
    number_of_country.add(country_dic[x[1]])

proxy_col.insert_many(list_proxies)


logger.info('Iteration complete\n')   

logger.info(f'Number of data: {number_of_ip}\n')
logger.info(f'Number of country: {len(number_of_country)}\n')
logger.info(f'Processing finished in {time.time() - start_time} seconds.\n')
