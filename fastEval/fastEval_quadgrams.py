import subprocess


#Quick evaluateQuadgrams function: 
#  Note - this function is only effective for longer plaintexts and/or many calls

def evaluateQuadgrams(process: subprocess.Popen, plaintext):
    #send plaintext to the process using stdin
    process.stdin.write(f"{plaintext}\n")
    process.stdin.flush()
    
    return float(process.stdout.readline())

def start_process(plaintext_len):
    return subprocess.Popen(
        ["./evaluateQuadgrams", str(plaintext_len)],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True
    )
    
def terminate(process):
    process.kill()

if __name__ == "__main__":
    plaintext = "helloworldthisisapieceofplaintexttobeevaluated"
    process = start_process(len(plaintext))

    print("fitness:", evaluateQuadgrams(process, plaintext))

    terminate(process)

