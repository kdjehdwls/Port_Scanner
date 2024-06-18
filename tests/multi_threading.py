import threading
from scan import port123_ntp, port445_smb, port902_vmware_soap, port3306_mysql

def run_scan(task, metadata, host, results):
    try:
        result = task(host)
        # port902_vmware_soap 함수의 결과가 리스트인 경우 처리
        if isinstance(result, list):
            results.extend(result)
        else:
            results.append(result)
    except Exception as e:
        error_result = {'port': metadata['port'], 'status': 'error', 'error_message': str(e)}
        results.append(error_result)

def scan_all(host):
    scan_tasks = [
        (port123_ntp, {'port': 123}),
        (port445_smb, {'port': 445}),
        (port902_vmware_soap, {'port': 902}),  # port902_vmware_soap 수정으로 인해 이제 902 포트만 스캔
        (port3306_mysql, {'port': 3306})
    ]

    threads = []
    results = []

    # 각 스캔 작업에 대한 스레드 생성 및 시작
    for task, metadata in scan_tasks:
        thread = threading.Thread(target=run_scan, args=(task, metadata, host, results))
        threads.append(thread)
        thread.start()

    # 모든 스레드가 완료될 때까지 기다립니다.
    for thread in threads:
        thread.join()

    # 결과를 포트 번호에 따라 정렬
    sorted_results = sorted(results, key=lambda x: x['port'])

    # 정렬된 결과 출력
    for result in sorted_results:
        print(result)

if __name__ == "__main__":
    host = '127.0.0.1' #'pool.ntp.org' #'127.0.0.1'
    scan_all(host)
