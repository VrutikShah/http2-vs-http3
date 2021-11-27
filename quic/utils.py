import os


def get_novel_name_server(novel_no:str) -> str:
    """
    Function to get the novel name given novel number.
    0 for test.txt and 1-5 for novel{1-5}.txt
    """
    root = "./data/"
    if novel_no == '0':
        root += "test.txt"
    else:
        root += f"novel{novel_no}.txt"
    return root

def get_downloaded_fname_client(novel_no: str, protocol:str) -> str:
    """
    get the name of the downloaded file as per naming convention {name}_{protocol}_{pid}.txt
    """
    client_pid = os.getpid()
    fname = "./downloads/"
    if novel_no == "0":
        fname += "test"
    else:
        fname += f"novel{novel_no}"
    fname += f"_{protocol}_{client_pid}.txt"
    return fname
