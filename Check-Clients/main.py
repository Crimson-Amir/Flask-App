import requests
from flask import Flask, render_template, request
import re
import datetime

auth = {'username': 'amir', 'password': 'amir'}

connect = requests.Session()
get_cookies = ""

if get_cookies == "":
    login = connect.post('https://admin.ggkala.shop:2053/login', data=auth)
    get_cookies = login.cookies.get('session')
    headers = {'Cookie': f'session={get_cookies}'}
    print(login.json())


app = Flask(__name__)


@app.route('/check_client', methods=['POST', 'GET'])
def check_client():
    if request.method == 'POST':
        message = request.form['message']
        email = request.form['email']
        conf = request.form['text']
        print("fyhhhhhhhhhhh", message)
        if message != "":
            with open('./admin/admin_text.txt', 'a') as e:
                e.write(f'\nmessage: {message}\nemail: {email}')
        try:
            is_full = True
            matches = re.findall(r'[^-]+$', str(conf))[-1]
            get_client = connect.get(
                f'https://admin.ggkala.shop:2053/panel/api/inbounds/getClientTraffics/{matches}', headers=headers)
            ret_conf = dict(get_client.json())

            # CLEAN DATA ---------------------
            if ret_conf['obj']['enable']:
                enable = 'Active ✅'
            else:
                enable = 'Inactive ❌'

            upload_gb = round(int(ret_conf['obj']['up']) / (1024 ** 3), 2)
            download_gb = round(int(ret_conf['obj']['down']) / (1024 ** 3), 2)
            usage_traffic = round(upload_gb + download_gb, 2)
            if int(ret_conf['obj']['total']) != 0:
                total_traffic = round(int(ret_conf['obj']['total']) / (1024 ** 3), 2)
            else:
                total_traffic = '∞'

            if ret_conf['obj']['expiryTime'] != 0:
                expiry_timestamp = ret_conf['obj']['expiryTime'] / 1000
                expiry_date = datetime.datetime.fromtimestamp(expiry_timestamp)
                expiry_month = expiry_date.strftime("%m/%d/%Y")
                days_lefts = (expiry_date - datetime.datetime.now()).days
            else:
                expiry_month = days_lefts = '∞'

            clean_data = {'enable': enable, 'expiry_month': expiry_month, 'upload_gb': upload_gb,
                          'download_gb': download_gb, 'usage_traffic': usage_traffic, 'total_traffic': total_traffic,
                          'days_left': days_lefts}

        except Exception:
            clean_data = {}
            is_full = False
            ret_conf = "Enter The Config"
        return render_template('master.html', is_full=is_full, config_=ret_conf, clean_data=clean_data)
    else:
        return render_template('master.html')


if __name__ == '__main__':
    app.run(debug=True)
