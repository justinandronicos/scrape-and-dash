## DEDUPE CODE
# if __name__ == "__main__":

#     optp = optparse.OptionParser()
#     optp.add_option(
#         "-v",
#         "--verbose",
#         dest="verbose",
#         action="count",
#         help="Increase verbosity (specify multiple times for more)",
#     )
#     (opts, args) = optp.parse_args()
#     log_level = logging.WARNING
#     if opts.verbose:
#         if opts.verbose == 1:
#             log_level = logging.INFO
#         elif opts.verbose >= 2:
#             log_level = logging.DEBUG
#     logging.getLogger().setLevel(log_level)

#     output_file = "data_matching_output.csv"
#     settings_file = "data_matching_learned_settings"
#     training_file = "data_matching_training.json"

#     # def descriptions():
#     #     for dataset in (products_prices, wm_products_prices):
#     #         for brand in dataset.keys():
#     #             for product in dataset[brand]:
#     #                 yield dataset[product]

#     def descriptions():
#         for dataset in (products_prices, wm_products_prices):
#             for id in dataset.keys():
#                 yield dataset[id]["product_name"]

#     if os.path.exists(settings_file):
#         print("reading from", settings_file)
#         with open(settings_file, "rb") as sf:
#             linker = dedupe.StaticRecordLink(sf)

#     else:

#         fields = [
#             {"field": "product_name", "type": "String"},
#             {"field": "product_name", "type": "Text", "corpus": descriptions()},
#             {"field": "retail_price", "type": "Price", "has missing": True},
#             # {"field": "current_price", "type": "Price", "has missing": True},
#             # {"field": "size", "type": "String", "has missing": True},
#             {"field": "brand", "type": "String", "has missing": True},
#         ]

#         linker = dedupe.RecordLink(fields)

#         if os.path.exists(training_file):
#             print("reading labeled examples from ", training_file)
#             with open(training_file) as tf:
#                 linker.prepare_training(
#                     products_prices,
#                     wm_products_prices,
#                     training_file=tf,
#                     sample_size=15000,
#                 )
#         else:
#             linker.prepare_training(
#                 products_prices, wm_products_prices, sample_size=2500
#             )

#             print("starting active labeling...")

#             dedupe.console_label(linker)

#             linker.train()

#             with open(training_file, "w") as tf:
#                 linker.write_training(tf)

#             with open(settings_file, "wb") as sf:
#                 linker.write_settings(sf)

#     print("clustering...")
#     linked_records = linker.join(products_prices, wm_products_prices, 0.0)

#     print("# duplicate sets", len(linked_records))

#     cluster_membership = {}
#     for cluster_id, (cluster, score) in enumerate(linked_records):
#         for record_id in cluster:
#             cluster_membership[record_id] = {
#                 "Cluster ID": cluster_id,
#                 "Link Score": score,
#             }

#         with open(output_file, "w") as f:

#             header_unwritten = True

#             for fileno, filename in enumerate((products_prices, wm_products_prices)):
#                 reader = filename

#                 if header_unwritten:

#                     fieldnames = [
#                         "Cluster ID",
#                         "Link Score",
#                         "source file",
#                     ] + reader.fieldnames

#                     writer = csv.DictWriter(f, fieldnames=fieldnames)
#                     writer.writeheader()

#                     header_unwritten = False

#                 for row_id, row in enumerate(reader):

#                     record_id = filename + str(row_id)
#                     cluster_details = cluster_membership.get(record_id, {})
#                     row["source file"] = fileno
#                     row.update(cluster_details)

#                     writer.writerow(row)
