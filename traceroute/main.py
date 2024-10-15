from pagermaid.enums import Message
from pagermaid.listener import listener
from pagermaid.utils import execute
import os
import re
import platform
import urllib.request

BESTTRACE_PATH = "/var/lib/pagermaid/plugins/besttrace"

@listener(
    is_plugin=False,
    command="t",
    need_admin=True,
    description="Perform a network trace using besttrace.",
    parameters="Provide the target to trace."
)
async def trace(message: Message):
    """Use besttrace to perform network tracing."""

    def extract_ip(text):
        ip_pattern = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
        match = ip_pattern.search(text)
        return match.group(0) if match else None

    def detect_architecture():
        """Detect system architecture and download the appropriate besttrace binary."""
        arch = platform.machine()
        # Debugging line to check the architecture
        print(f"Detected architecture: {arch}")

        # Add more architectures as needed
        if arch in ["x86_64"]:
            url = "https://raw.githubusercontent.com/midori01/PagerMaid-Plugins/v2/traceroute/besttraceamd"
        elif arch in ["aarch64"]:
            url = "https://raw.githubusercontent.com/midori01/PagerMaid-Plugins/v2/traceroute/besttracearm"
        else:
            raise Exception(f"Unsupported architecture: {arch}")

        # Download the binary if not already present
        if not os.path.exists(BESTTRACE_PATH):
            try:
                urllib.request.urlretrieve(url, BESTTRACE_PATH)
                os.chmod(BESTTRACE_PATH, 0o755)  # Make the file executable
            except Exception as e:
                raise Exception(f"Error downloading besttrace: {str(e)}")

    # Detect and download besttrace binary if needed
    try:
        detect_architecture()
    except Exception as e:
        await message.edit(f"Error: {str(e)}")
        return

    target = message.arguments

    if not target and message.reply_to_message:
        target = extract_ip(message.reply_to_message.text or "")

    if not target:
        await message.edit("Error: No target specified or no IP found in the replied message.")
        return

    command = f"{BESTTRACE_PATH} -g cn -q 1 {target}"

    try:
        result = await execute(command)
    except Exception as e:
        await message.edit(f"Error executing command: {str(e)}")
        return

    if result:
        result_lines = result.splitlines()
        if len(result_lines) > 1:
            result = "\n".join(result_lines[1:])

        title = f"**Traceroute to {target}**"
        final_result = f"{title}\n```\n{result}\n```"
        await message.edit(final_result)
    else:
        await message.edit("No result returned from the trace.")