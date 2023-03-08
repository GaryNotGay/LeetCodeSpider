import re
import json
import requests

# 20230306 total 2962

def ERRORINFO(function, exception, extrainfo):
    print(f"[ERROR INFO] function:{function}, exception:{exception}, extrainfo:{extrainfo}")

def getQuestionList(start, total):
    try:
        skip = start
        limit = 100
        res = []
        while skip < start+total:
            u = "https://leetcode.cn/graphql/"
            d = {"query":"\n    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {\n  problemsetQuestionList(\n    categorySlug: $categorySlug\n    limit: $limit\n    skip: $skip\n    filters: $filters\n  ) {\n    hasMore\n    total\n    questions {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId\n      isFavor\n      paidOnly\n      solutionNum\n      status\n      title\n      titleCn\n      titleSlug\n      topicTags {\n        name\n        nameTranslated\n        id\n        slug\n      }\n      extra {\n        hasVideoSolution\n        topCompanyTags {\n          imgUrl\n          slug\n          numSubscribed\n        }\n      }\n    }\n  }\n}\n    ","variables":{"categorySlug":"","skip":skip,"limit":limit,"filters":{}}}
            c = {"LEETCODE_SESSION": LEETCODE_SESSION}
            r = requests.post(url=u, cookies=c, json=d)
            rj = json.loads(r.content.decode("utf-8"))
            res += rj["data"]["problemsetQuestionList"]["questions"]
            skip += limit
        return res[:total]
    except Exception as e:
        ERRORINFO("getAllQuesNum", e, f"total={start, total}")

def getSolution(type, questionSlug):
    try:
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"questionSolutionArticles","variables":{"questionSlug":f"{questionSlug}","first":10,"skip":0,"orderBy":"DEFAULT","tagSlugs":[type],"userInput":""},"query":"query questionSolutionArticles($questionSlug: String!, $skip: Int, $first: Int, $orderBy: SolutionArticleOrderBy, $userInput: String, $tagSlugs: [String!]) {\n  questionSolutionArticles(questionSlug: $questionSlug, skip: $skip, first: $first, orderBy: $orderBy, userInput: $userInput, tagSlugs: $tagSlugs) {\n    totalNum\n    edges {\n      node {\n        ...solutionArticle\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment solutionArticle on SolutionArticleNode {\n  ipRegion\n  rewardEnabled\n  canEditReward\n  uuid\n  title\n  slug\n  sunk\n  chargeType\n  status\n  identifier\n  canEdit\n  canSee\n  reactionType\n  reactionsV2 {\n    count\n    reactionType\n    __typename\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    tagType\n    __typename\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    profile {\n      userAvatar\n      userSlug\n      realName\n      __typename\n    }\n    __typename\n  }\n  summary\n  topic {\n    id\n    commentCount\n    viewCount\n    __typename\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  isEditorsPick\n  hitCount\n  videosInfo {\n    videoId\n    coverUrl\n    duration\n    __typename\n  }\n  __typename\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        if len(rj["data"]["questionSolutionArticles"]["edges"]):
            slug = rj["data"]["questionSolutionArticles"]["edges"][0]["node"]["slug"]
            title = rj["data"]["questionSolutionArticles"]["edges"][0]["node"]["title"]
        else:
            d = {"operationName": "questionSolutionArticles",
                 "variables": {"questionSlug": f"{questionSlug}", "first": 10, "skip": 0, "orderBy": "DEFAULT",
                               "tagSlugs": [""], "userInput": ""},
                 "query": "query questionSolutionArticles($questionSlug: String!, $skip: Int, $first: Int, $orderBy: SolutionArticleOrderBy, $userInput: String, $tagSlugs: [String!]) {\n  questionSolutionArticles(questionSlug: $questionSlug, skip: $skip, first: $first, orderBy: $orderBy, userInput: $userInput, tagSlugs: $tagSlugs) {\n    totalNum\n    edges {\n      node {\n        ...solutionArticle\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment solutionArticle on SolutionArticleNode {\n  ipRegion\n  rewardEnabled\n  canEditReward\n  uuid\n  title\n  slug\n  sunk\n  chargeType\n  status\n  identifier\n  canEdit\n  canSee\n  reactionType\n  reactionsV2 {\n    count\n    reactionType\n    __typename\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    tagType\n    __typename\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    profile {\n      userAvatar\n      userSlug\n      realName\n      __typename\n    }\n    __typename\n  }\n  summary\n  topic {\n    id\n    commentCount\n    viewCount\n    __typename\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  isEditorsPick\n  hitCount\n  videosInfo {\n    videoId\n    coverUrl\n    duration\n    __typename\n  }\n  __typename\n}\n"}
            r = requests.post(url=u, cookies=c, json=d)
            rj = json.loads(r.content.decode("utf-8"))
            slug = rj["data"]["questionSolutionArticles"]["edges"][0]["node"]["slug"]
            title = rj["data"]["questionSolutionArticles"]["edges"][0]["node"]["title"]

        d = {"operationName":"solutionDetailArticle","variables":{"slug":f"{slug}","orderBy":"DEFAULT"},"query":"query solutionDetailArticle($slug: String!, $orderBy: SolutionArticleOrderBy!) {\n  solutionArticle(slug: $slug, orderBy: $orderBy) {\n    ...solutionArticle\n    content\n    question {\n      questionTitleSlug\n      __typename\n    }\n    position\n    next {\n      slug\n      title\n      __typename\n    }\n    prev {\n      slug\n      title\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment solutionArticle on SolutionArticleNode {\n  ipRegion\n  rewardEnabled\n  canEditReward\n  uuid\n  title\n  slug\n  sunk\n  chargeType\n  status\n  identifier\n  canEdit\n  canSee\n  reactionType\n  reactionsV2 {\n    count\n    reactionType\n    __typename\n  }\n  tags {\n    name\n    nameTranslated\n    slug\n    tagType\n    __typename\n  }\n  createdAt\n  thumbnail\n  author {\n    username\n    profile {\n      userAvatar\n      userSlug\n      realName\n      __typename\n    }\n    __typename\n  }\n  summary\n  topic {\n    id\n    commentCount\n    viewCount\n    __typename\n  }\n  byLeetcode\n  isMyFavorite\n  isMostPopular\n  isEditorsPick\n  hitCount\n  videosInfo {\n    videoId\n    coverUrl\n    duration\n    __typename\n  }\n  __typename\n}\n"}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        content = rj["data"]["solutionArticle"]["content"]
        return slug, title, content

    except Exception as e:
        ERRORINFO("getSolution", e, f"questionSlug={questionSlug}")

def getQuestionDetail(titleSlug):
    try:
        res = ""
        difficulty = {"Easy":"简单", "Medium":"中等", "Hard":"困难"}
        u = "https://leetcode.cn/graphql/"
        d = {"operationName":"questionData","variables":{"titleSlug":titleSlug},"query":"query questionData($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    questionId\n    questionFrontendId\n    categoryTitle\n    boundTopicId\n    title\n    titleSlug\n    content\n    translatedTitle\n    translatedContent\n    isPaidOnly\n    difficulty\n    likes\n    dislikes\n    isLiked\n    similarQuestions\n    contributors {\n      username\n      profileUrl\n      avatarUrl\n      __typename\n    }\n    langToValidPlayground\n    topicTags {\n      name\n      slug\n      translatedName\n      __typename\n    }\n    companyTagStats\n    codeSnippets {\n      lang\n      langSlug\n      code\n      __typename\n    }\n    stats\n    hints\n    solution {\n      id\n      canSeeDetail\n      __typename\n    }\n    status\n    sampleTestCase\n    metaData\n    judgerAvailable\n    judgeType\n    mysqlSchemas\n    enableRunCode\n    envInfo\n    book {\n      id\n      bookName\n      pressName\n      source\n      shortDescription\n      fullDescription\n      bookImgUrl\n      pressImgUrl\n      productUrl\n      __typename\n    }\n    isSubscribed\n    isDailyQuestion\n    dailyRecordStatus\n    editorType\n    ugcQuestionId\n    style\n    exampleTestcases\n    jsonExampleTestcases\n    __typename\n  }\n}\n"}
        c = {"LEETCODE_SESSION": LEETCODE_SESSION}
        r = requests.post(url=u, cookies=c, json=d)
        rj = json.loads(r.content.decode("utf-8"))
        rjj = json.loads(rj["data"]["question"]["stats"])
        label = ""
        for l in rj["data"]["question"]["topicTags"]:
            if l["translatedName"] is None:
                label += "None"
                label += "、"
            else:
                label += l["translatedName"]
                label += "、"
        res += f"\n\n# {rj['data']['question']['questionId']}.{rj['data']['question']['translatedTitle']}\nhttps://leetcode.cn/problems/{titleSlug}/\n\n困难度：{difficulty[rj['data']['question']['difficulty']]}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过率：{rjj['acRate']}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;标签：{label[:-1]}\n"
        res += "\n\n## English\n\n---\n"
        res += rj["data"]["question"]["content"]
        if "hints" in rj["data"]["question"].keys() and rj["data"]["question"]["hints"] != []:
            res += "\n\n### hint\n"
            for hint in rj["data"]["question"]["hints"]:
                res += f"\n>{hint}\n"
        res += "\n\n## 中文翻译\n\n---\n"
        if rj["data"]["question"]["translatedContent"] is None:
            res += "无"
        else:
            res += rj["data"]["question"]["translatedContent"]
        if rj["data"]["question"]["categoryTitle"] == "Database":
            solutionContent = getSolution("", titleSlug)
            res += "\n\n## Database题解\n\n---\n"
        elif rj["data"]["question"]["categoryTitle"] == "Shell":
            solutionContent = getSolution("", titleSlug)
            res += "\n\n## Shell题解\n\n---\n"
        else:
            solutionContent = getSolution("python3", titleSlug)
            res += "\n\n## Python3题解\n\n---\n"
        res += f"\n>https://leetcode.cn/problems/{titleSlug}/solution{solutionContent[0]}, {solutionContent[1]}\n"
        res += solutionContent[2]
        return res

    except Exception as e:
        ERRORINFO("getQuestionDetail", e, f"titleSlug={titleSlug}")





LEETCODE_SESSION = ""
DEBUG = False


if not DEBUG:
    path = r"C:"
    questionList = getQuestionList(1, 2962)
    for question in questionList:
        try:
            titleSlug = question["titleSlug"]
            if not question['titleCn'] == "":
                bookName = f"{question['frontendQuestionId']}.{question['titleCn']}"
            else:
                bookName = f"{question['frontendQuestionId']}.{question['title'].replace(' ', '.')}"
            questionDetail = getQuestionDetail(titleSlug)
            with open(f"{path}\\{bookName}.md", 'w', encoding="utf-8") as f:
                f.write(questionDetail)
            f.close()
            print(f"{bookName} Done")
        except:
            print(f"{bookName} Failed")
else:
    c = getQuestionDetail("")

