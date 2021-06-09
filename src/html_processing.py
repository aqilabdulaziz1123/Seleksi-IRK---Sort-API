# Function to make an html page for the specified algorithm
def sorting_page(algoritma, token):
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset='utf-8'>
            <title>{algoritma} Sort</title>
        </head>
        <body>
            <form action="/sort/{algoritma.lower()}?token={token}" method="post" enctype="multipart/form-data">
                <label for="csv_file">Enter CSV File : </label>
                <input type="file" name="csv_file"/><br><br>
                <label for="column_no">Enter Column No. : (Starts from 1)</label>
                <input type="text" name="column_no"/><br><br>
                <label for="orientation">Sorting Orientation : </label>
                <input type="radio" id="asc" name="orientation" value="ascending"/>
                <label for="asc">Ascending</label>
                <input type="radio" id="desc" name="orientation" value="descending"/>
                <label for="desc">Descending</label><br><br>
                <input type="submit" value="Submit"/><br><br>
                <a href='/mainpage?token={token}'>Back to Main Menu</a>
            </form>
        </body>
    </html>
    """

def log_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset='utf-8'>
            <title>Login</title>
        </head>
        <body>
            <form action="/login" method="post" enctype="multipart/form-data">
                <label for="username">Username : </label>
                <input type="text" name="username"/><br><br>
                <label for="password">Password : </label>
                <input type="text" name="password"/><br><br>
                <input type="submit" value="Login"/><br><br>
                <a href='/'>Back to Main Menu</a>
            </form>
        </body>
    </html>
    """

def sign_page():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset='utf-8'>
            <title>Signup</title>
        </head>
        <body>
            <form action="/signup" method="post" enctype="multipart/form-data">
                <label for="username">Username : </label>
                <input type="text" name="username"/><br><br>
                <label for="password">Password : </label>
                <input type="text" name="password"/><br><br>
                <label for="name">Name : </label>
                <input type="text" name="name"/><br><br>
                <input type="submit" value="Signup"/><br><br>
                <a href='/'>Back to Main Menu</a>
            </form>
        </body>
    </html>
    """

# Function to turn a list into an html table
def list_to_table(l):
    header = l[0]
    body = l[1:]

    table_script = f"""
    <table class="dataframe" border="1">
        <tbody>
            <tr style="text-align: center">
    """
    for colname in header:
        table_script += f"""
                <th>{colname}</th>
        """
    
    table_script += """
            </tr>
        """

    for row in body:
        table_script += """
            <tr style="text-align: center">
        """
        for col in row:
            table_script += f"""
                <td>{col}</td>
            """
        table_script += """
            </tr>
        """
    table_script += """
        </tbody>
    </table>
    """
    return table_script
