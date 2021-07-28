
class FileConverter:
    @staticmethod
    def text_to_list(file):
        text = file.decode("UTF8")

        list = text.split("\n")

        for i in range(len(list)):
            list[i] = list[i].replace("\r", '')

        for i in range(len(list)):
            list[i] = list[i].split(",")

        return list

    @staticmethod
    def list_to_text(list):
        text = ''

        for i in range(len(list)):
            list[i] = ",".join(list[i])

        text = text + "\r\n".join(list)

        return text

    @staticmethod
    def list_to_table(data_list):
        table = "<table>\n"

        table += "<thead>\n"
        table += "<tr>\n"

        for i in range(len(data_list[0])):
            table += "<th style='text-align: left;'>" + \
                str(data_list[0][i]) + "</th>\n"

        table += "</tr>\n"
        table += "</thead>\n"

        table += "<tbody>\n"

        for i in range(1, len(data_list)):
            table += "<tr>\n"
            for j in range(len(data_list[i])):
                table += "<td>" + str(data_list[i][j]) + "</td>\n"
            table += "</tr>\n"

        table += "</tbody>\n"

        table += "</table>\n"

        return table
