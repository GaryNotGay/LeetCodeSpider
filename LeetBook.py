import re
import os
import json
import requests


def ERRORINFO(function, exception, extrainfo):
    print(f"[ERROR INFO] function:{function}, exception:{exception}, extrainfo:{extrainfo}")

def getBookName(bookSlug):
    try:
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"leetbookDetail","variables":{"bookSlug":bookSlug},"query":"query leetbookDetail($bookSlug: String!) {\n  leetbookBookDetail(bookSlug: $bookSlug) {\n    ...leetbookDetailNode\n    __typename\n  }\n}\n\nfragment leetbookDetailNode on LeetbookDetailBookNode {\n  id\n  slug\n  title\n  coverImg\n  description\n  ownedType\n  visibility\n  isFavorite\n  totalStudied\n  chapterNum\n  pageNum\n  premiumOnlyPageNum\n  readTime\n  workStatus\n  subjects {\n    name\n    __typename\n  }\n  author {\n    realName\n    title\n    bio\n    avatar\n    userSlug\n    __typename\n  }\n  progress {\n    numCompleted\n    numCompletedPremium\n    startedAt\n    __typename\n  }\n  productInfo {\n    allowBorrow\n    premiumOnly\n    product {\n      id\n      slug\n      price\n      hasPremiumPrice\n      premiumPrice\n      discounts {\n        id\n        availableAfter\n        availableBefore\n        price\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  descBlocks {\n    content\n    title\n    type\n    __typename\n  }\n  summary {\n    content\n    type\n    __typename\n  }\n  commonTags {\n    nameTranslated\n    name\n    slug\n    tagType\n    __typename\n  }\n  forSaleAt\n  companyForm {\n    company {\n      name\n      slug\n      __typename\n    }\n    windowName\n    formTitle\n    formDesc\n    formFields {\n      displayName\n      keyName\n      valueType\n      valueMaxLimit\n      required\n      order\n      placeholder\n      options {\n        key\n        label\n        __typename\n      }\n      __typename\n    }\n    myExtraInfo\n    displayInLbDetail\n    displayBeforeOwning\n    __typename\n  }\n  __typename\n}\n"}
        r = requests.post(url=u, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        return rj["data"]["leetbookBookDetail"]["title"]
    except Exception as e:
        ERRORINFO("getBookName", e, f"bookSlug={bookSlug}")

def markCompleted(pageId):
    try:
        u = "https://leetcode.cn/graphql/"
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        h = {"referer": "https://leetcode.cn/"}
        d = {"operationName":"leetbookMarkAsCompleted","variables":{"pageId":pageId},"query":"mutation leetbookMarkAsCompleted($pageId: ID!) {\n  leetbookMarkAsCompleted(pageId: $pageId) {\n    ok\n    __typename\n  }\n}\n"}
        r = requests.post(url=u, cookies=c, headers=h, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        return rj["data"]["leetbookMarkAsCompleted"]["ok"]
    except Exception as e:
        ERRORINFO("markCompleted", e, f"pageId={pageId}")


def getCode(uuid):
    try:
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"fetchPlayground","variables":{},"query":"query fetchPlayground {\n  playground(uuid: \""+uuid+"\") {\n    testcaseInput\n    name\n    isUserOwner\n    showRunCode\n    showOpenInPlayground\n    selectedLangSlug\n    isShared\n    __typename\n  }\n  allPlaygroundCodes(uuid: \"cnmXjHuH\") {\n    code\n    langSlug\n    __typename\n  }\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        res = ""
        for lan in rj["data"]["allPlaygroundCodes"]:
            name = rj["data"]["playground"]["name"] + "-" + lan["langSlug"]
            res += f"\n\n>{name}\n"
            res += "\n```\n"
            res += lan["code"]
            res += "\n```\n"
        return res
    except Exception as e:
        ERRORINFO("getCode", e, f"uuid={uuid}")

def getPageList(bookSlug):
    try:
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"leetbookCatalog","variables":{"bookSlug":bookSlug},"query":"query leetbookCatalog($bookSlug: String!) {\n  leetbookBookDetail(bookSlug: $bookSlug) {\n    id\n    title\n    coverImg\n    ownedType\n    pages(showDraft: true) {\n      ...leetbookPageInfoNode\n      __typename\n    }\n    productInfo {\n      allowBorrow\n      premiumOnly\n      product {\n        price\n        premiumPrice\n        hasPremiumPrice\n        __typename\n      }\n      __typename\n    }\n    author {\n      realName\n      userSlug\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment leetbookPageInfoNode on LeetbookPageInfoNode {\n  title\n  id\n  pageType\n  prerequisite {\n    id\n    title\n    pageType\n    __typename\n  }\n  premiumOnly\n  isSample\n  isDraft\n  isTitleHidden\n  parentId\n  order\n  qaQuestionUuid\n  publishedAt\n  isGreyTitle\n  __typename\n}\n"}
        r = requests.post(url=u, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        pageDetail = rj["data"]["leetbookBookDetail"]["pages"][::-1]
        pageList = []
        for page in pageDetail:
            if not page["parentId"]:
                pageList.append(page)
            else:
                for i in pageDetail:
                    if i["id"] == page["parentId"]:
                        if not "childList" in i.keys():
                            i["childList"] = []
                        i["childList"].append(page)
        return sorted(pageList, key=lambda e: e["order"])
    except Exception as e:
        ERRORINFO("getPageList", e, f"bookSlug={bookSlug};page={page};i={i}")

def getPageDetail(pageId):
    try:
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"leetbookPageDetail","variables":{"pageId":pageId},"query":"query leetbookPageDetail($pageId: ID!) {\n  leetbookPage(pageId: $pageId) {\n    title\n    subtitle\n    id\n    pageType\n    blocks {\n      type\n      value\n      __typename\n    }\n    commonTags {\n      nameTranslated\n      name\n      slug\n      __typename\n    }\n    qaQuestionUuid\n    ...leetbookQuestionPageNode\n    __typename\n  }\n}\n\nfragment leetbookQuestionPageNode on LeetbookQuestionPage {\n  question {\n    questionId\n    envInfo\n    judgeType\n    metaData\n    enableRunCode\n    sampleTestCase\n    judgerAvailable\n    langToValidPlayground\n    questionFrontendId\n    style\n    content\n    translatedContent\n    questionType\n    questionTitleSlug\n    editorType\n    mysqlSchemas\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    topicTags {\n      slug\n      name\n      translatedName\n      __typename\n    }\n    jsonExampleTestcases\n    __typename\n  }\n  __typename\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        res = ""
        if rj["data"]["leetbookPage"]["pageType"] == "PROGRAMMING_QUESTION":
            url = f'https://leetcode.cn/problems/{rj["data"]["leetbookPage"]["question"]["questionTitleSlug"]}/'
            res += f"\n>{url}\n"
            res += rj["data"]["leetbookPage"]["question"]["translatedContent"]
        elif rj["data"]["leetbookPage"]["pageType"] == "MIXED" or rj["data"]["leetbookPage"]["pageType"] == "CHAPTER":
            for block in rj["data"]["leetbookPage"]["blocks"]:
                if block["type"] == "HTML" or "MARKDOWN":
                    rawStr = block["value"]
                    for uuid in re.findall(pattern="<iframe frameborder=\"0\" height=\"300\" src=\"https://leetcode-cn.com/playground/(.*)//shared\" width=\"100%\"></iframe>", string=rawStr):
                        rawStr = rawStr.replace(f'<iframe frameborder="0" height="300" src="https://leetcode-cn.com/playground/{uuid}//shared" width="100%"></iframe>', getCode(uuid))
                    res += rawStr
        return res
    except Exception as e:
        ERRORINFO("getPageDetail", e, f"pageId={pageId};block={block}")

def genMarkdown(level, pageList):
    try:
        markdownStr = ""
        for page in pageList:
            preTitle = "#"*level
            markdownStr += f"\n{preTitle} {page['title']}\n"
            if "prerequisite" in page.keys():
                if not page["prerequisite"] is None:
                    markCompleted(page["prerequisite"]["id"])
            markdownStr += f"{getPageDetail(page['id'])}\n"
            if "childList" in page.keys():
                markdownStr += genMarkdown(level+1, sorted(page["childList"], key=lambda e: e["order"]))
                markdownStr += "\n"
        return markdownStr
    except Exception as e:
        ERRORINFO("genMarkdown", e, f"level={level};page={page}")

def purchaseFreeBook(ids):
    try:
        u = "https://leetcode.cn/graphql/noj-go"
        d = {"operationName": "leetbooksByIds", "variables": {"ids": [ids]},"query": "query leetbooksByIds($ids: [Int!]) {\n  leetbooksByIds(bookIds: $ids) {\n    id\n    slug\n    title\n    coverImg\n    description\n    totalStudied\n    recommendation\n    totalStudied\n    ownedType\n    author {\n      user {\n        realName\n        userSlug\n        userAvatar\n        __typename\n      }\n      title\n      bio\n      __typename\n    }\n    chapterNum\n    pageNum\n    progress {\n      numCompleted\n      numCompletedPremium\n      accessedAt\n      __typename\n    }\n    productInfo {\n      premiumOnly\n      allowBorrow\n      product {\n        id\n        slug\n        price\n        premiumPrice\n        discounts {\n          id\n          availableAfter\n          availableBefore\n          price\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    forSaleAt\n    lastNewPageForSaleAt\n    commonTags {\n      nameTranslated\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        bookId = rj["data"]["leetbooksByIds"][0]["id"]
        if rj["data"]["leetbooksByIds"][0]["ownedType"] == "PURCHASED":
            return True
        if rj["data"]["leetbooksByIds"][0]["productInfo"]["allowBorrow"]:
            d = {"operationName":"leetbookBorrowBook","variables":{"bookId":bookId},"query":"mutation leetbookBorrowBook($bookId: ID!) {\n  leetbookBorrowBook(bookId: $bookId) {\n    ok\n    error\n    __typename\n  }\n}\n"}
        else:
            d = {"operationName":"leetbookPurchaseFreeBook","variables":{"bookId":bookId},"query":"mutation leetbookPurchaseFreeBook($bookId: ID!) {\n  leetbookPurchaseFreeBook(bookId: $bookId) {\n    ok\n    error\n    __typename\n  }\n}\n"}
        u = "https://leetcode.cn/graphql/"
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        return rj["data"]["leetbookPurchaseFreeBook"]["ok"]
    except Exception as e:
        ERRORINFO("purchaseFreeBook", e, f"ids={ids}")

def checkPermission(bookSlug):
    try:
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"leetbookDetail","variables":{"bookSlug":bookSlug},"query":"query leetbookDetail($bookSlug: String!) {\n  leetbookBookDetail(bookSlug: $bookSlug) {\n    ...leetbookDetailNode\n    __typename\n  }\n}\n\nfragment leetbookDetailNode on LeetbookDetailBookNode {\n  id\n  slug\n  title\n  coverImg\n  description\n  ownedType\n  visibility\n  isFavorite\n  totalStudied\n  chapterNum\n  pageNum\n  premiumOnlyPageNum\n  readTime\n  workStatus\n  subjects {\n    name\n    __typename\n  }\n  author {\n    realName\n    title\n    bio\n    avatar\n    userSlug\n    __typename\n  }\n  progress {\n    numCompleted\n    numCompletedPremium\n    startedAt\n    __typename\n  }\n  productInfo {\n    allowBorrow\n    premiumOnly\n    product {\n      id\n      slug\n      price\n      hasPremiumPrice\n      premiumPrice\n      discounts {\n        id\n        availableAfter\n        availableBefore\n        price\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  descBlocks {\n    content\n    title\n    type\n    __typename\n  }\n  summary {\n    content\n    type\n    __typename\n  }\n  commonTags {\n    nameTranslated\n    name\n    slug\n    tagType\n    __typename\n  }\n  forSaleAt\n  companyForm {\n    company {\n      name\n      slug\n      __typename\n    }\n    windowName\n    formTitle\n    formDesc\n    formFields {\n      displayName\n      keyName\n      valueType\n      valueMaxLimit\n      required\n      order\n      placeholder\n      options {\n        key\n        label\n        __typename\n      }\n      __typename\n    }\n    myExtraInfo\n    displayInLbDetail\n    displayBeforeOwning\n    __typename\n  }\n  __typename\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        if rj["data"]["leetbookBookDetail"]["productInfo"]["allowBorrow"]:
            return True
        elif rj["data"]["leetbookBookDetail"]["ownedType"] == "PURCHASED" or rj["data"]["leetbookBookDetail"]["ownedType"] == "BORROWED":
            return True
        elif not rj["data"]["leetbookBookDetail"]["productInfo"]["product"]["price"]:
            return True
        else:
            return False
    except Exception as e:
        ERRORINFO("checkPermission", e, f"bookSlug={bookSlug}")

def getBookId(ids):
    try:
        u = "https://leetcode.cn/graphql/noj-go"
        d = {"operationName":"leetbooksByIds","variables":{"ids":[ids]},"query":"query leetbooksByIds($ids: [Int!]) {\n  leetbooksByIds(bookIds: $ids) {\n    id\n    slug\n    title\n    coverImg\n    description\n    totalStudied\n    recommendation\n    totalStudied\n    ownedType\n    author {\n      user {\n        realName\n        userSlug\n        userAvatar\n        __typename\n      }\n      title\n      bio\n      __typename\n    }\n    chapterNum\n    pageNum\n    progress {\n      numCompleted\n      numCompletedPremium\n      accessedAt\n      __typename\n    }\n    productInfo {\n      premiumOnly\n      allowBorrow\n      product {\n        id\n        slug\n        price\n        premiumPrice\n        discounts {\n          id\n          availableAfter\n          availableBefore\n          price\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    forSaleAt\n    lastNewPageForSaleAt\n    commonTags {\n      nameTranslated\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        return rj["data"]["leetbooksByIds"][0]["slug"]
    except Exception as e:
        ERRORINFO("getBookId", e, f"ids={ids}")

def getAllBookNumId():
    try:
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"leetbookCategories","variables":{},"query":"query leetbookCategories {\n  leetbookCategories {\n    id\n    name\n    subcategories {\n      bookIds\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        res = []
        for category in rj["data"]["leetbookCategories"]:
            for subcategory in category["subcategories"]:
                res += eval(subcategory["bookIds"])
        return res
    except Exception as e:
        ERRORINFO("getAllBookNumId", e, f"")

LEETCODE_SESSION = ""
DEBUG = False

if not DEBUG:
    path = r"C:"
    bookSlug = getBookId(ids)
    if checkPermission(bookSlug):
        #purchaseFreeBook(ids)
        pageList = getPageList(bookSlug)
        markdownStr = genMarkdown(1, pageList)
        bookName = getBookName(bookSlug)
        if not os.path.exists(f"{path}\\{bookName}.md"):
            with open(f"{path}\\{bookName}.md", 'w', encoding="utf-8") as f:
                f.write(markdownStr)
            f.close()
            print(f"{[bookSlug]} Done")
        else:
            print(f"{[bookSlug]} Exist")
    else:
        print(f"{[bookSlug]} Deny")

else:
    bookid = markCompleted("")

