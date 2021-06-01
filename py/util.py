def validate(args):
  if "column" in args:
    col = args["column"]
    if not col.isnumeric() or int(col) < 0:
      return None, None, "Bad arguments (column id invalid)"
  else:
    return None, None, "Bad arguments (column id should be specified)"

  if "order" in args:  
    order = args["order"]
    if order != "ASC" or order != "DESC":
      return None, None, "Bad arguments (order should be ASC or DESC)"
  else:
    order = "ASC"

  return int(col), order, None