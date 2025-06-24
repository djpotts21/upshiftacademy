"""views.py
Handles the logic for running code challenges,
executing student code against test cases,
and rendering results in the template."""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import CodeChallenge, CodeSubmission
from .forms import CodeSubmissionForm
from .judge0 import submit_code_to_judge0, get_submission_result
# pylint: disable=unspecified-encoding, exec-used, unused-variable, no-member
# # flake8: noqa: E402, F841


def parse_python_error(stderr):
    """Parse Python error messages to provide user-friendly feedback."""
    if "NameError" in stderr:
        parts = stderr.strip().split(":")
        if len(parts) >= 2:
            return f"❌ Error: {parts[-1].strip()}\n\n💡 Tip: Check if the function or variable is defined."
        return "❌ NameError: Check for missing function or variable definitions."
    
    if "SyntaxError" in stderr:
        return "❌ Syntax Error: Please check your code formatting and punctuation."

    if "IndentationError" in stderr:
        return "❌ Indentation Error: Python relies on consistent spacing."

    if "TypeError" in stderr:
        return f"❌ {stderr.strip().splitlines()[-1]}"
 
    return stderr.strip() or ""


def parse_python_output(output):
    """Parse Python output to provide user-friendly feedback."""
    if not output:
        return "❌ No output generated."

    lines = output.strip().splitlines()
    if len(lines) == 1:
        return lines[0].strip()

    return "\n".join(line.strip() for line in lines if line.strip())


def parse_python_result(result):
    """Parse the result from Judge0 to determine if the code passed."""
    if not result:
        return "No result available."
    if "Accepted" in result:
        return "✅ Accepted"
    elif "Wrong Answer" in result:
        return "❌ Wrong Answer"
    elif "Time Limit Exceeded" in result:
        return "⏳ Time Limit Exceeded"
    elif "Runtime Error" in result:
        return "❌ Runtime Error"
    else:
        return f"❓ {result}"


def run_code_challenge(request, challenge_id):
    """Run a code challenge by executing student code against test cases."""
    challenge = get_object_or_404(CodeChallenge, pk=challenge_id)
    result = error = output = ""
    user_friendly_error = ""

    if request.method == "POST":
        print("Form submitted")
        print("Student code:", request.POST.get("code"))
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            token = submit_code_to_judge0(code, challenge.test_code)
            judge_result = get_submission_result(token)
            raw_error = judge_result.get("stderr") or ""
            user_friendly_error = parse_python_error(raw_error)

            output = parse_python_output(judge_result.get("stdout", ""))
            error = judge_result.get("stderr", "")
            status = judge_result.get(
                "status", {}).get("description", "Unknown")

            passed = (
                "Accepted" in status and (
                    not challenge.expected_output or
                    output.strip() == challenge.expected_output.strip()
                )
            )

            CodeSubmission.objects.create(
                challenge=challenge,
                student=request.user,
                code=code,
                output=output,
                error=error,
                passed=passed,
            )

            result = f"✅ {status}" if passed else f"❌ {status}"
    else:
        form = CodeSubmissionForm()

    return render(request, "challenges/code_challenge.html", {
        "challenge": challenge,
        "form": form,
        "result": result,
        "output": output,
        "error": error,
        "user_friendly_error": user_friendly_error
    })


def run_code_ajax(request, challenge_id):
    """Run code challenge via AJAX, submitting code and returning results."""
    if request.method == "POST" and request.headers.get(
        "x-requested-with") == "XMLHttpRequest":
        code = request.POST.get("code", "")
        challenge = CodeChallenge.objects.get(pk=challenge_id)

        try:
            token = submit_code_to_judge0(code, challenge.test_code)
            judge_result = get_submission_result(token)
            raw_error = judge_result.get("stderr") or ""
            user_friendly_error = parse_python_error(raw_error)
            
        except Exception as e:
            import traceback
            traceback.print_exc()  # Logs to console
            return JsonResponse({"error": f"Code execution failed: {str(e)}"}, status=500)

        output = parse_python_output(judge_result.get("stdout", ""))
        error = judge_result.get("stderr") or ""
        status = judge_result.get("status", {}).get("description", "Unknown")
        result = parse_python_result(status)
        user_friendly_error = user_friendly_error

        passed = "accepted" in status.lower() and (
            not challenge.expected_output or output.strip(
                ) == challenge.expected_output.strip()
        )

        # Save submission only if student is logged in
        if request.user.is_authenticated:
            CodeSubmission.objects.create(
                challenge=challenge,
                student=request.user,
                code=code,
                output=output,
                error=error,
                passed=passed,
            )

        return JsonResponse({
            "result": result,
            "output": output,
            "error": error,
            "passed": passed,
            "user_friendly_error": user_friendly_error
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
