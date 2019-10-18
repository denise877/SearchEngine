import webbrowser

def handleHtml (title,alist) :
    result = \
    '''	
    <html>
    <head>
		<meta charset="UTF-8">
		<meta name="Search Result" content="Login Page">
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<meta name="author" content="Peng Zhou, Yaoqi Li">

		<title>Search Results</title>
	</head>
	<body><br>
	<div id="container" style="width: 1000px; margin: 0 auto">
	<h1>Search result for '''
    result += title + "<h2><br>\n"
    for i in range(len(alist)) :
        result += "<h3><a href='http://" + alist[i][0] + "'>" + alist[i][1] + "</a></h3><p>" + alist[i][0] + "</p><br>"
    result += "</div></body></html>"

    #file = open("/tmp/result.html","w")
    file = open("C:\\Users\\rdfzz\\AppData\\Local\\Temp\\result.html","w")
    file.write(result)
    file.close()
    #webbrowser.open_new_tab("file:///tmp/result.html")
    webbrowser.open_new_tab("C:\\Users\\rdfzz\\AppData\\Local\\Temp\\result.html")
    
