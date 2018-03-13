#储存查询结果后的文书
legalDocuments=[]
countResults={}
resultCount=0
allSearchField=["dsrxx","ah","spry","ysfycm","ysqqqk","byrw","spjg","ysdbqk","esqqqk","ysfyrw","ajms","xgft","sprq","sljg","bycm","sjy","bt"]
allSearchFieldList={"当事人信息":"dsrxx","案号":"ah","审判日期":"spry","一审法院查明":"ysfycm","一审请求情况":"ysqqqk","本院认为":"byrw","审理经过":"spjg","一审答辩情况":"ysdbqk","二审请求情况":"esqqqk","一审法院认为":"ysfyrw","案件描述":"ajms","相关法条":"xgft","审判日期":"sprq","审理经过":"sljg","本院查明":"bycm","书记员":"sjy","标题":"bt"}
allSearchFieldListR={"dsrxx":"当事人信息","ah":"案号","spry":"审判日期","ysfycm":"一审法院查明","ysqqqk":"一审请求情况","byrw":"本院认为","spjg":"审理经过","ysdbqk":"一审答辩情况","esqqqk":"二审请求情况","ysfyrw":"一审法院认为","案件描述":"ajms","xgft":"相关法条","sprq":"审判日期","sljg":"审理经过","bycm":"本院查明","sjy":"书记员","bt":"标题"}