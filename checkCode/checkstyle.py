import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def checkCode(code):
    generateFile(code)
    result = excuteCMD()
    return result


def generateFile(code):
    try:
         with open("checkCode/Check.java", "w") as f:
            f.write(code)
    except Exception as err:
        print err, "error found\n"


def excuteCMD():
    codeResults=[]
    # env_dist = os.environ
    # for key in env_dist:
    #     print key + ' : ' + env_dist[key]
    # os.popen("java com.puppycrawl.tools.checkstyle.Main -c doc/google_checks.xml -o build/error check.java")
    # p = os.popen("java com.puppycrawl.tools.checkstyle.Main -c doc/google_checks.xml check.java")
    os.popen("cd checkCode&&java com.puppycrawl.tools.checkstyle.Main -c doc/google_checks.xml -o build/error check.java")
    p = os.popen("cd checkCode&&java com.puppycrawl.tools.checkstyle.Main -c doc/google_checks.xml check.java")
    results = p.readlines()
    results = results[1:-1]
    for result in results:
        index = result.find("check.java")
        if index>0:
            result = result[0:7] + "Line" +result[index+10:-1]
        print result
        codeResults.append(result)

    return codeResults


if __name__ == "__main__":
    # code='''import com.puppycrawl.tools.checkstyle.Main;public class Check {public static void main(String[] args) {System.out.println("hi");if(true){if(true){if(true){if(true){}}'''
    # checkCode(code)
    excuteCMD()