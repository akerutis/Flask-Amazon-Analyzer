import chart_studio.plotly as py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from numpy.ma import var

py.sign_in("Muffles", "n7fnqiXZVX9eIO8YVhOq")

customer_list = []
useful_customer = []
fileName=None
unique_states=[]
state_count=[]
moneylist=[]


def reset():
    customer_list.clear()
    useful_customer.clear()
    unique_states.clear()
    state_count.clear()
    moneylist.clear()

def get_map():
    df = pd.read_csv("State_List.csv")
    for col in df.columns:
        df[col] = df[col].astype(str)

    scl = [[0.0, 'rgb(255, 255, 255)'], [1.0, 'rgb(255, 0, 0)']]

    df['text'] = df['State'] + '<br>' +\
        'Count '+df['Count'] + 'Money '+df['Money']



    return df

    fig = go.Figure(data=go.Choropleth(
            type='choropleth',
            colorscale=scl,
            autocolorscale=False,
            locations=df['State'],
            z=df['Count'].astype(float),
            locationmode='USA-states',
            text=df['text'],
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )
            ),
            colorbar=dict(
                title="Order Number "
            )
        ))

    fig.update_layout(
            title_text = 'Customer Orders by State',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)',
            ),
        )

    return fig

    fig = px.choropleth(locations=df['State'], locationmode="USA-states", color=df['Count'].astype(float),
                        color_continuous_scale="Viridis", range_color=(0, 12),  scope="usa",
                        labels={'unemp':'unemployment rate'}, title = 'Customer Orders by State')

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    #fig.show()


def get_data(file_name):
    from model.Customer import Customer
    import csv
    from itertools import groupby

    with open(("static/img/uploads/" + file_name), 'r', encoding='utf-8') as f:
        reader = csv.reader(f, dialect='excel', delimiter='\t')
        for row in reader:
            if len(row) == 30:
                row.extend([""])
                row.extend([""])

            if len(row) == 31:
                row.extend([""])

            if len(row) < 32 or len(row) > 32:
                print(len(row))
                print(row + "was not processed")

            customer_list.append(
                Customer(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10],
                         row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20],
                         row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30],
                         row[31]))
    # for name in customer_list:
    #    print(name.ship_city)
    print(len(customer_list))

    states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS',
              'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV',
              'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

    us_state_abbrev = {
        'ALABAMA': 'AL',
        'ALASKA': 'AK',
        'ARIZONA': 'AZ',
        'ARKANSAS': 'AR',
        'CALIFORNIA': 'CA',
        'CA.': 'CA',
        'COLORADO': 'CO',
        'CONNECTICUT': 'CT',
        'DELAWARE': 'DE',
        'FLORIDA': 'FL',
        'GEORGIA': 'GA',
        'HAWAII': 'HI',
        'IDAHO': 'ID',
        'ILLINOIS': 'IL',
        'INDIANA': 'IN',
        'IOWA': 'IA',
        'KANSAS': 'KS',
        'KENTUCKY': 'KY',
        'LOUISIANA': 'LA',
        'MAINE': 'ME',
        'MARYLAND': 'MD',
        'MASSACHUSETTS': 'MA',
        'MICHIGAN': 'MI',
        'MINNESOTA': 'MN',
        'MISSISSIPPI': 'MS',
        'MISSOURI': 'MO',
        'MONTANA': 'MT',
        'NEBRASKA': 'NE',
        'NEVADA': 'NV',
        'NEW HAMPSHIRE': 'NH',
        'NEW JERSEY': 'NJ',
        'NEW MEXICO': 'NM',
        'NEW YORK': 'NY',
        'NORTH CAROLINA': 'NC',
        'NORTH DAKOTA': 'ND',
        'OHIO': 'OH',
        'OKLAHOMA': 'OK',
        'OREGON': 'OR',
        'PENNSYLVANIA': 'PA',
        'RHODE ISLAND': 'RI',
        'SOUTH CAROLINA': 'SC',
        'SOUTH DAKOTA': 'SD',
        'TENNESSEE': 'TN',
        'TEXAS': 'TX',
        'UTAH': 'UT',
        'VERMONT': 'VT',
        'VIRGINIA': 'VA',
        'WASHINGTON': 'WA',
        'WEST VIRGINIA': 'WV',
        'WISCONSIN': 'WI',
        'WYOMING': 'WY',
    }

    all_states = []
    for cus in customer_list:
        if cus.item_price != "":
            if not(cus.ship_state.upper() in states):
                stater = cus.ship_state.upper()
                name = (us_state_abbrev.get(stater, "skipped"))
                if name == "skipped":
                    print(stater + " was skipped")
                else:
                    all_states.append(name)
            else:
                all_states.append(cus.ship_state.upper())
    all_states.sort()
    print(all_states)
    unique_states = all_states
    unique_states = list(set(unique_states))
    unique_states.sort()
    print(unique_states)
    state_count = [len(list(group)) for key, group in groupby(all_states)]
    print(state_count)
    moneylist = [0]*len(unique_states)

    for cus in customer_list:
        if cus.item_price != "":
            for index in range(len(unique_states)):
                if cus.ship_state.upper() == unique_states[index] or us_state_abbrev.get(cus.ship_state.upper(), "invalid") == unique_states[index]:
                    try:
                        moneylist[index] += float(cus.item_price)
                    except:
                        print("yikes")
    with open('State_List.csv', 'w') as csvfile:
        fieldnames = ['State', 'Count', 'Money']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(unique_states)):
            moneylist[i] = round(moneylist[i],2)
            writer.writerow({'State': unique_states[i], 'Count': state_count[i], 'Money': moneylist[i]})
            useful_customer.append([unique_states[i], state_count[i], moneylist[i]])
    return(unique_states,moneylist,state_count)

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


def get_promotions():
    promos = []
    for cus in customer_list:
        if cus.promotion_ids != "" and cus.promotion_ids != "promotion-ids" and isfloat(cus.item_price):
            check = False
            for index in promos:
                if index[0] == cus.promotion_ids:
                    index[1] += float(cus.item_price)
                    check = True
            if not check and float(cus.item_price)>0:
                promos.append([cus.promotion_ids, float(cus.item_price)])
    return promos


def process():
    us_state_abbrev = {
        'ALABAMA': 'AL',
        'ALASKA': 'AK',
        'ARIZONA': 'AZ',
        'ARKANSAS': 'AR',
        'CALIFORNIA': 'CA',
        'CA.': 'CA',
        'COLORADO': 'CO',
        'CONNECTICUT': 'CT',
        'DELAWARE': 'DE',
        'FLORIDA': 'FL',
        'GEORGIA': 'GA',
        'HAWAII': 'HI',
        'IDAHO': 'ID',
        'ILLINOIS': 'IL',
        'INDIANA': 'IN',
        'IOWA': 'IA',
        'KANSAS': 'KS',
        'KENTUCKY': 'KY',
        'LOUISIANA': 'LA',
        'MAINE': 'ME',
        'MARYLAND': 'MD',
        'MASSACHUSETTS': 'MA',
        'MICHIGAN': 'MI',
        'MINNESOTA': 'MN',
        'MISSISSIPPI': 'MS',
        'MISSOURI': 'MO',
        'MONTANA': 'MT',
        'NEBRASKA': 'NE',
        'NEVADA': 'NV',
        'NEW HAMPSHIRE': 'NH',
        'NEW JERSEY': 'NJ',
        'NEW MEXICO': 'NM',
        'NEW YORK': 'NY',
        'NORTH CAROLINA': 'NC',
        'NORTH DAKOTA': 'ND',
        'OHIO': 'OH',
        'OKLAHOMA': 'OK',
        'OREGON': 'OR',
        'PENNSYLVANIA': 'PA',
        'RHODE ISLAND': 'RI',
        'SOUTH CAROLINA': 'SC',
        'SOUTH DAKOTA': 'SD',
        'TENNESSEE': 'TN',
        'TEXAS': 'TX',
        'UTAH': 'UT',
        'VERMONT': 'VT',
        'VIRGINIA': 'VA',
        'WASHINGTON': 'WA',
        'WEST VIRGINIA': 'WV',
        'WISCONSIN': 'WI',
        'WYOMING': 'WY',
    }

    global player1
    player1 = var.get()
    sum_state = 0

    for index in useful_customer:
        if index[0] == player1.upper() or index[0] == us_state_abbrev.get(player1.upper(), "Invalid"):
            sum_state = float(index[2])


def create_pie():
    name_list= []
    asin_list = []
    for cus in customer_list:
        if cus.asin != "" and cus.asin.lower() != "asin":
            asin_list.append(cus.asin)
    unique_asin = asin_list
    unique_asin = list(set(unique_asin))

    for index in unique_asin:
        for cus in customer_list:
            if index == cus.asin:
                name_list.append(cus.product_name)
                break

    print(unique_asin)

    sum_asin = [0] * len(unique_asin)
    for cus in customer_list:
        if cus.item_price != "":
            for index in range(len(unique_asin)):
                if cus.asin == unique_asin[index]:
                    sum_asin[index] += float(cus.item_price)

    sum_all = 0
    for index in sum_asin:
        sum_all += float(index)


    print(sum_asin)
    sum_all=round(sum_all, 2)
    unique_asin = asin_list
    unique_asin = list(set(unique_asin))

    for first in range(len(sum_asin)):
        for index in range(first, len(sum_asin)):
            if(sum_asin[first]<sum_asin[index]):
                temp = sum_asin[first]
                sum_asin[first] = sum_asin[index]
                sum_asin[index] = temp
                temp2 = unique_asin[first]
                unique_asin[first] = unique_asin[index]
                unique_asin[index] = temp2
                temp3 = name_list[first]
                name_list[first] = name_list[index]
                name_list[index] = temp3


    percents = []
    for index in range(len(sum_asin)):
        percents.append(str('{:.2f}'.format(100*float(sum_asin[index])/float(sum_all))))
    """
    labels = [""]*(len(unique_asin))

    for i in range(len(unique_asin)):
        labels[i] = "(" + percents[i] + "%)   " + name_list[i] + "\n ASIN: " + unique_asin[i]


    sizes = sum_asin
    colors = ['red', 'green', 'orange', 'teal', 'blue', 'gray', 'yellow', 'black', 'magenta', 'cyan']

    plt.clf()
    plt.cla()
    plt.close()
    gs = gridspec.GridSpec(2, 1)
    ax1 = plt.subplot(gs[0, 0])
    ax1.pie(sizes, colors=colors, shadow=True, startangle=90)
    ax1.axis('equal')
    ax1.legend(labels=labels, bbox_to_anchor=(0,0), loc="upper left")
    fig = plt.gcf()
    fig.set_size_inches(15, 8)
    """
    return sum_all, percents, name_list, unique_asin

def browsefunc():

    try:


        outpromo = get_promotions()
        last_element = []
        for index in outpromo:
            temp = index[0].split(',')
            if len(temp) > 1:
                index[0] = ""
                for i in range(len(temp)):
                    if i == (len(temp) - 1):
                        last_element.append(str(temp[i]))
                    else:
                        index[0] += temp[i] + " + \n"
            else:
                last_element.append(str(index[0]))
                index[0] = ""

        promo={}
        for index in range(len(outpromo)):
           promo[("{:<55}".format(last_element[index]))] = "${:<40}".format(
               str('{:.2f}'.format(outpromo[index][1])))

        return promo



    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)

        print("Error", "An Error Occurred, please restart the application and try again with another file")


        return




