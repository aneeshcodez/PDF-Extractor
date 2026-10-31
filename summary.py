def final_summary(successful_invoices,error_invoices):
    print(f"Total number of files processed : {len(successful_invoices) + len(error_invoices)} ")
    print(f"Total number of files succeeded : {len(successful_invoices)}")
    print(f"Total number of files failed : {len(error_invoices)}")