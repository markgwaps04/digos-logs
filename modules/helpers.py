from django.core.handlers.wsgi import WSGIRequest
from django.http.request import QueryDict
from django.utils.html import escape
from django.db.models.query import RawQuerySet
from datetime import date, datetime, timezone;
from django.db.models.base import ModelBase


class ValidationError(Exception):
     """ Raise if one of the field thrown error"""

class InvalidRequest(Exception):
     """ Raise if request is not valid"""

class AlreadyExist(Exception):
    """ Raise if already been exist"""

class EmptySequence(Exception):
    """ Raise Cannot choose from an empty sequence """
    pass;

class QuizDone(Exception):
    """ Raise if the quiz is already done"""
    pass;


class StudentActivity(Exception):
    """ Raise if the quiz is already done"""
    pass;


class message:
    VALIDATION_ERROR = "Validation Error";
    INVALID_REQUEST = "Invalid Request";
    SUCCESS = "Success";

class of_date:

    @staticmethod
    def getCurrentTimeStamp():

        dt = datetime.now();
        timestamp = dt.replace(tzinfo=timezone.utc).timestamp();
        return int(timestamp);

        pass;

    pass;

class _String:

    @staticmethod
    def format_by_paragraph(value : str):
        of_value = str(value).split("\r\n");
        formatStr = "";
        for per in of_value : formatStr +="<p>" + per + "</p>";
        return formatStr;

    @staticmethod
    def int_to_roman(num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ];

        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ];

        roman_num = '';
        i = 0;
        while num > 0:
            for _ in range(num // val[i]):
                roman_num += syb[i];
                num -= val[i];
                pass;
            i +=1;

        return roman_num;

        pass;



class _Model:

    def __init__(self, model: ModelBase):

        if not hasattr(model, "_check_model"):
            raise AttributeError("Invalid Attribute");

        self.model = model;

        pass;

    @staticmethod
    def getFields(model: ModelBase):

        if not hasattr(model, "_check_model"):
            raise AttributeError("Invalid Attribute");

        _thatModel = model._meta.local_fields
        _thatModel = [f.name for f in _thatModel];

        return list(_thatModel);

        pass;

    def getValue(self):

        fields = self.getFields(self.model);
        partial = dict();
        for f in fields:

            that_value = getattr(self.model, str(f));

            if hasattr(that_value, "_check_model"):
                that_value = that_value.__str__();

            if isinstance(that_value, (datetime, date)):
                that_value = that_value.isoformat();

            partial[f] = that_value;

        return partial;

    pass;


class _JSON:

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, list):
            for per in obj:  obj[per] = _JSON.json_serial(per);
            pass;

        if isinstance(obj, (datetime, date)):
            return obj.isoformat();

        # raise TypeError("Type %s not serializable" % type(obj))


class _ofString:
    @staticmethod
    def sql_where(ofDict: dict):

        partial = "";
        keys = list(ofDict.keys());
        for every in keys[:-1]:
            partial += "`" + every + "`= '" + str(ofDict[every]) + "' and ";
        else:
            partial += "`" + keys[-1] + "`= '" + str(ofDict[keys[-1]]) + "'";

        return partial;

        pass;


class _RawQuerySet:

    @staticmethod
    def toList(data: RawQuerySet):
        partial = [];

        for every in data:
            ofDict = dict(every.__dict__);
            del ofDict["_state"];
            partial.append(ofDict);

        return partial;


class _ofDict:
    value: dict = dict();

    def __init__(self, param: dict):

        self.value = param;

    @staticmethod
    def removeEmpty(value: dict):

        if not isinstance(value, dict):
            raise TypeError("parameter 1 not valid type");

        # print(value. n

        for item in dict(value):

            if not value[item]: del value[item]

        return value;

    def checkHasKeys(self, param: list) -> bool:

        keys = self.value.keys();
        keys = list(keys);

        keys.sort();
        param.sort();

        return keys == param;

    def get_difference_list(self, param: list) -> list:

        keys = self.value.keys();
        keys = list(keys);

        difference = [item for item in param if item not in keys]
        return difference;

        pass;


class _QueryDict:

    @staticmethod
    def toDict(ofDict: QueryDict) -> dict:
        ofDict = dict(ofDict.lists());
        obj = dict();

        for items in ofDict:
            obj[items] = ofDict[items][0] \
                if (len(ofDict[items]) > 0) \
                else None;

        return obj;


class _ofList:

    @staticmethod
    def onlyKeys(array : list,listOf : list):

        partial = [];

        for item in array:

            if not isinstance(item,dict): raise AttributeError('Invalid value');
            obj = dict();

            for value in listOf:

                if not value in item : raise AttributeError('Invalid keys');
                obj[value] = item[value];

            partial.append(obj);

            pass;

        return partial;


    pass;


class constraint_filter_keys:
    base: dict = dict();
    store: dict = dict();


class constraint:
    request_value = None;
    POST_value = None;
    GET_value = None;
    FILE_values = None;
    data = [];

    def __init__(self, request: WSGIRequest, method=None):

        if not isinstance(request, WSGIRequest):
            raise TypeError("Parameter 1 invalid type");

        self.__request = request;
        self.POST_value = request.POST;
        self.GET_value = request.GET;
        self.FILE_values = request.FILES;

        self.request_value = getattr(request, method) \
            if method \
            else request.POST \
                if request.method == "POST" \
                else request.GET;

        pass;

    def check(self, arr: list, removeEmpty: bool = False) -> dict:

        try:
            self.strict(arr,removeEmpty);
            return True;
        except AttributeError as e:
            return False;
        except InvalidRequest as e:
            return False;
            pass;

        pass;

    def safe(self, of_dict : dict, un_strict = False):
        of_data = self.request_value;
        of_data = _QueryDict.toDict(of_data);

        for per in list(of_dict.keys()):
            value = of_dict[per];
            if value :
                if (not per in of_data) or (not str(of_data[per]).strip()) :
                    raise InvalidRequest("Invalid value, " + str(per) + "=" +str(value));
                pass;
            elif un_strict and value == False and not (per in of_data):

                # self.request_value is return QueryDict
                # to make editable the query dict _mutable = True

                self.request_value._mutable = True;
                self.request_value.appendlist(per, None);
                self.request_value._mutable = False;
                pass;
            pass;

        return self.strict(list(of_dict.keys()),False);
        pass;

    def strict(self, arr: list, removeEmpty: bool) -> dict:

        ofRaw = arr;
        ofRaw = self.filter_keys(ofRaw);
        ofRaw = self.htmlspecialchars(ofRaw);

        if removeEmpty: ofRaw = _ofDict.removeEmpty(ofRaw);
        selfDict = _ofDict(ofRaw);

        check = selfDict.checkHasKeys(arr);

        if not check:
            print("Difference lists")
            print(selfDict.get_difference_list(arr));
            raise InvalidRequest("Does not supply a valid parameters");

        self.data = ofRaw;
        return ofRaw;

        pass;

    def htmlspecialchars(self, value=None) -> dict:

        if not value:
            value = self.request_value;
            value = _QueryDict.toDict(value);

        for items in value:
            if value[items]:
                value[items] = escape(value[items]);

        return value;

    def filter_keys(self, store: list, value: dict = None) -> dict:

        if not isinstance(store, list):
            raise TypeError("parameter 1 not valid type");

        if not value:
            value = self.request_value;
            value = _QueryDict.toDict(value);

        ofVal = dict();

        for item in store:
            if item in value: ofVal[item] = value[item];
            continue;

        return ofVal;

        pass;

    @staticmethod
    def session_set_pages(request : WSGIRequest):

        if not isinstance(request, WSGIRequest):
            raise TypeError("Parameter 1 invalid type");

        if not ("pages" in request.session): request.session['pages'] = [];

        FULL_URL_WITH_QUERY_STRING = request.build_absolute_uri()
        FULL_URL = request.build_absolute_uri('?')
        ABSOLUTE_ROOT = request.build_absolute_uri('/')[:-1].strip("/")
        ABSOLUTE_ROOT_URL = request.build_absolute_uri('/').strip("/");
        REQUEST_PATH = request.get_full_path();

        if len(request.session['pages']) > 0 \
                and (request.session['pages'][0] == REQUEST_PATH): return;


        request.session['pages'].append(REQUEST_PATH);
        request.session['pages'].reverse();

        # request.session['pages'] = list(set(request.session['pages']));

        pass;
