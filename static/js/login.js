var contrApp = angular.module('loginApp', []);
if (navigator.userAgent.toLowerCase().indexOf("chrome") >= 0) {

	$(window).load(function() {
		$('input:-webkit-autofill').each(function() {
			var text = $(this).val();
			var name = $(this).attr('name');
			$(this).after(this.outerHTML).remove();
			$('input[name=' + name + ']').val(text);
		});
	});
}
contrApp.controller("loginCtr", [
		"$scope",
		"$http",
		function($scope, $http) {
			var tuser = $.cookie("systemuser");
			if (angular.isDefined(tuser)) {
				$scope.email = tuser;
			}

			$scope.isremb = true;
			$scope.errorTxt = "";
			$scope.login = function() {
				if ($scope.password != $("#password").val()) {
					$scope.password = $("#password").val();
				}
				if ($scope.email != $("#email").val()) {
					$scope.email = $("#email").val();
				}
				var params = {
					"email" : $scope.email,
					"password" : $scope.password
				};
				if (!$scope.email || params.email == '') {
					$scope.errorTxt = "请输入用户名";
					return false;
				}

				if (!$scope.password || params.password == '') {
					$scope.errorTxt = "请输入密码";
					return false;
				}

				var isOnline = $scope.isremb == true ? "1" : "0";
				$http.post("api/find/login?isOnline=" + isOnline, params)
						.success(function(data, status) {
							if (status == 200) {
								$scope.errorTxt = "登录成功";
								if ($scope.isremb) {
									setCookie('systemuser', params.email, 7);
									setCookie('systemuserid', data.id, 7);
								} else {
									setCookie('systemuserid', data.id, 1);
								}
								window.location.href = "/index.html";
							} else {
								$scope.errorTxt = "用户名或密码错误";
							}
						}).error(function(data, status) {
							$scope.errorTxt = "用户名或密码错误";
						});

			}

			$scope.keyEvt = function(e) {
				if (e.keyCode == 13) {
					$scope.login();
				}
			}

			function setCookie(n, _value, d) {
				$.cookie(n, _value, {
					expires : d,
					path : '/',
					secure : false,
					raw : false
				});
			}
		} ]);
